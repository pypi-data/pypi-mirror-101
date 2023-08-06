from hestia_earth.schema import IndicatorJSONLD

from .utils import _linked_node, _aggregated_version


def _new_indicator(term: dict):
    indicator = IndicatorJSONLD().to_dict()
    indicator['term'] = _linked_node(term)
    return _aggregated_version(indicator, 'value', 'term')
