from hestia_earth.schema import SchemaType, TermTermType
from hestia_earth.utils.api import find_node, find_node_exact

SEARCH_LIMIT = 10000
DEFAULT_COUNTRY_NAME = 'World'


def _fetch_all(term_type: TermTermType): return find_node(SchemaType.TERM, {'termType': term_type.value}, SEARCH_LIMIT)


def _fetch_single(term_id: str): return find_node_exact(SchemaType.TERM, {'name': term_id})


def _fetch_default_country(): return _fetch_single(DEFAULT_COUNTRY_NAME)
