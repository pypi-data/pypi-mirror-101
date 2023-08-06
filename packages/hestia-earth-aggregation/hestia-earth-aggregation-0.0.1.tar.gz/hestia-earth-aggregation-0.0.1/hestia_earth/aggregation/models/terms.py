from hestia_earth.schema import TermTermType
from hestia_earth.utils.tools import non_empty_list

from hestia_earth.aggregation.log import logger
from hestia_earth.aggregation.utils import _average, _aggregated_version
from hestia_earth.aggregation.term_utils import _fetch_all
from hestia_earth.aggregation.impact_assessment_utils import _create_impact_assessment
from hestia_earth.aggregation.indicator_utils import _new_indicator

AGGREGATION_KEY = 'emissionsResourceUse'


def _all_terms():
    return _fetch_all(TermTermType.EMISSION) + _fetch_all(TermTermType.RESOURCEUSE)


def _aggregate_indicators(term: dict, indicators: list, product: dict):
    values = [indicator.get('value') for indicator in indicators]
    indicator = _new_indicator(term)
    logger.debug('product=%s, term: %s, values: %s',
                 product.get('@id'), term.get('@id'), ', '.join([str(v) for v in values]))
    indicator['value'] = _average(values)
    return _aggregated_version(indicator)


def _aggregate_term(product: dict, indicators_map: dict):
    def aggregate(term: dict):
        indicators = indicators_map.get(term.get('@id'), [])
        return _aggregate_indicators(term, indicators, product) if len(indicators) > 0 else None
    return aggregate


def _aggregate_impact(impact_data: dict, aggregates: list):
    impact = _create_impact_assessment(impact_data)
    impact[AGGREGATION_KEY] = aggregates
    return impact


def _aggregate_impacts(terms: list):
    def aggregate(data: dict):
        aggregates = non_empty_list(map(_aggregate_term(data.get('product'), data.get('indicators')), terms))
        return _aggregate_impact(data.get('impacts')[0], aggregates) if len(aggregates) > 0 else None
    return aggregate


def aggregate(impacts_per_product: dict) -> list:
    terms = _all_terms()
    return non_empty_list(map(_aggregate_impacts(terms), impacts_per_product.values()))
