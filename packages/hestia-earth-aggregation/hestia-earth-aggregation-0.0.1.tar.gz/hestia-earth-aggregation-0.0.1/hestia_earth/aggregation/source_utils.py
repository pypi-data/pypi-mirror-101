from hestia_earth.schema import SchemaType
from hestia_earth.utils.api import find_node_exact

from .utils import _linked_node

HESTIA_BIBLIO_TITLE = 'Hestia: A new data platform for storing and analysing data on the productivity \
and sustainability of agriculture'


def _get_source():
    source = find_node_exact(SchemaType.SOURCE, {'bibliography.title': HESTIA_BIBLIO_TITLE})
    return _linked_node(source) if source else None
