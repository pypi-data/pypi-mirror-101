from hestia_earth.utils.tools import non_empty_list

from hestia_earth.aggregation.log import logger
from hestia_earth.aggregation.utils import _aggregated_version, _flatten
from hestia_earth.aggregation.impact_assessment_utils import _create_impact_assessment, _impact_assessment_year
from hestia_earth.aggregation.indicator_utils import _new_indicator

AGGREGATION_KEY = 'emissionsResourceUse'


def _aggregate_indicators(country_id: str, year: int, term: dict, indicators: list, product: dict):
    value = sum([indicator.get('value') for indicator in indicators])
    indicator = _new_indicator(term)
    logger.debug('product=%s, country=%s, year=%s, term: %s, value: %s',
                 product.get('@id'), country_id, str(year), term.get('@id'), str(value))
    indicator['value'] = value
    return _aggregated_version(indicator)


def _aggregate_world_impact(data: dict):
    product = data.get('product')
    impacts = data.get('impacts', [])
    impact = impacts[0]
    country_id = impact.get('country').get('@id')
    year = _impact_assessment_year(impact)

    def aggregate(term_id: str):
        indicators = data.get('indicators').get(term_id)
        term = indicators[0].get('term')
        return _aggregate_indicators(country_id, year, term, indicators, product)

    aggregates = _flatten(map(aggregate, data.get('indicators', {}).keys()))
    impact = _create_impact_assessment(impact)
    impact['organic'] = False
    impact['irrigated'] = False
    impact[AGGREGATION_KEY] = aggregates
    return impact if len(aggregates) > 0 else None


def aggregate(impacts_per_product: dict) -> list:
    return non_empty_list([
        _aggregate_world_impact(value) for value in impacts_per_product.values()
    ])
