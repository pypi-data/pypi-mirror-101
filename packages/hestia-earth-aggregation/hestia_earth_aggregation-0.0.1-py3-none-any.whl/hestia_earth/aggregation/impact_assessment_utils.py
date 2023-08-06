from functools import reduce
import requests
import json
from concurrent.futures import ThreadPoolExecutor
from hestia_earth.schema import SchemaType
from hestia_earth.utils.api import download_hestia, find_node
from hestia_earth.utils.tools import non_empty_list, safe_parse_date
from hestia_earth.utils.request import api_url

from .log import logger
from .utils import _linked_node
from .term_utils import DEFAULT_COUNTRY_NAME, _fetch_single
from .source_utils import HESTIA_BIBLIO_TITLE

SEARCH_LIMIT = 10000
# exclude ImpactAssessment from ecoinvent
EXCLUDE_BIBLIOS = [
    HESTIA_BIBLIO_TITLE,
    'The ecoinvent database version 3 (part I): overview and methodology'
]


def _all_impacts(country_name: str):
    headers = {'Content-Type': 'application/json'}
    must_queries = [{'match': {'@type': SchemaType.IMPACTASSESSMENT.value}}]
    must_not_queries = list(map(lambda title: {'match': {'source.bibliography.title.keyword': title}}, EXCLUDE_BIBLIOS))
    if country_name != DEFAULT_COUNTRY_NAME:
        must_queries.append({'match': {'country.name.keyword': country_name}})

    query = {
        'bool': {
            'must': must_queries,
            'must_not': must_not_queries
        }
    }
    logger.debug('Running query: %s', json.dumps(query))
    return requests.post(f"{api_url()}/search", json.dumps({
        'query': query,
        'limit': SEARCH_LIMIT,
        'fields': ['@id']
    }), headers=headers).json().get('results', [])


def _download_impact(data_state=''):
    def download(n):
        try:
            node = download_hestia(n.get('@id'), SchemaType.IMPACTASSESSMENT, data_state=data_state)
            return node if node.get('@type') else None
        except Exception:
            logger.debug('skip non-%s impact_assessment: %s', data_state, n.get('@id'))
            return None
    return download


def _download_impacts(impacts: list, data_state=''):
    total = len(impacts)
    with ThreadPoolExecutor() as executor:
        impacts = non_empty_list(executor.map(_download_impact(data_state), impacts))
    logger.debug('downloaded %s impacts / %s total impacts', str(len(impacts)), str(total))
    return impacts


def _all_impacts_by_product(country_name: str):
    # TODO: paginate search and improve performance
    impacts = _all_impacts(country_name)
    impacts = _download_impacts(impacts, data_state='recalculated')
    return _group_impacts_by_product(impacts)


def _global_impacts_by_product():
    impacts = find_node(SchemaType.IMPACTASSESSMENT, {'source.bibliography.title.keyword': HESTIA_BIBLIO_TITLE})
    impacts = _download_impacts(impacts)
    return _group_impacts_by_product(impacts, False)


def _group_indicators(group: dict, indicator: dict):
    term_id = indicator.get('term').get('@id')
    if term_id not in group:
        group[term_id] = []
    group[term_id].append(indicator)
    return group


def _group_impacts_by_product(impacts: list, include_matrix=True) -> dict:
    def group_by(group: dict, impact: dict):
        organic = impact.get('organic', False)
        irrigated = impact.get('irrigated', False)
        key = '-'.join([
            str(organic),
            str(irrigated),
            impact.get('product').get('@id')
        ]) if include_matrix else impact.get('product').get('@id')
        if key not in group:
            group[key] = {
                'product': impact.get('product'),
                # save first impact to get fields
                # TODO: might not be the best approach?
                'impacts': [],
                'indicators': {}
            }
        group[key]['impacts'].append(impact)
        indicators = impact.get('emissionsResourceUse', [])
        # save ref to organic/irrigated for later grouping
        indicators = list(map(lambda v: {**v, 'organic': organic, 'irrigated': irrigated}, indicators))
        indicators = reduce(_group_indicators, indicators, group[key]['indicators'])
        group[key]['indicators'] = indicators
        return group

    return reduce(group_by, impacts, {})


def _impact_assessment_year(impact: dict):
    date = safe_parse_date(impact.get('endDate'))
    return date.year if date else None


def _impact_assessment_id(n: dict, include_matrix=True):
    # TODO: handle impacts that dont have organic/irrigated version => only 1 final version
    return '-'.join(non_empty_list([
        n.get('product', {}).get('@id'),
        n.get('country', {}).get('name'),
        n.get('endDate'),
        ('organic' if n.get('organic', False) else 'conventional') if include_matrix else '',
        ('irrigated' if n.get('irrigated', False) else 'non-irrigated') if include_matrix else ''
    ]))


def _impact_assessment_name(n: dict, include_matrix=True):
    return ', '.join(non_empty_list([
        n.get('product', {}).get('name'),
        n.get('country', {}).get('name'),
        n.get('endDate'),
        '-'.join(non_empty_list([
            ('Organic' if n.get('organic', False) else 'Conventional') if include_matrix else '',
            ('Irrigated' if n.get('irrigated', False) else 'Non Irrigated') if include_matrix else ''
        ]))
    ]))


def _create_impact_assessment(data: dict):
    impact = {'type': SchemaType.IMPACTASSESSMENT.value}
    # copy properties from existing ImpactAssessment
    impact['endDate'] = data['endDate']
    impact['product'] = _linked_node(data['product'])
    impact['functionalUnitMeasure'] = data['functionalUnitMeasure']
    impact['functionalUnitQuantity'] = data['functionalUnitQuantity']
    impact['allocationMethod'] = data['allocationMethod']
    impact['systemBoundary'] = data['systemBoundary']
    impact['organic'] = data.get('organic', False)
    impact['irrigated'] = data.get('irrigated', False)
    impact['dataPrivate'] = False
    if data.get('country'):
        impact['country'] = data['country']
    if data.get('source'):
        impact['source'] = data['source']
    return impact


def _update_impact_assessment(country_name, source: dict = None, include_matrix=True):
    def update(impact: dict):
        country = _fetch_single({'name': country_name}) if isinstance(country_name, str) else country_name
        impact['country'] = _linked_node({
            **country,
            '@type': SchemaType.TERM.value
        })
        impact['name'] = _impact_assessment_name(impact, include_matrix)
        impact['id'] = _impact_assessment_id(impact, include_matrix)
        return impact if source is None else {**impact, 'source': source}
    return update


def _remove_duplicated_impact_assessments(impacts: list):
    def filter_impact(impact: dict):
        # removes non-organic + non-irrigated original impacts (they are recalculated by country average)
        return impact.get('organic', False) or impact.get('irrigated', False) \
            or 'conventional-non-irrigated' not in impact.get('id')

    return list(filter(filter_impact, impacts))
