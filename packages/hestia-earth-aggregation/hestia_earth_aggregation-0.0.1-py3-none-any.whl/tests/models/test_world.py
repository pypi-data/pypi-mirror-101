import unittest
import json

from tests.utils import fixtures_path
from hestia_earth.aggregation.models.world import aggregate
from hestia_earth.aggregation.impact_assessment_utils import _group_impacts_by_product, _update_impact_assessment

class_path = 'hestia_earth.aggregation.models.world'


class TestWorld(unittest.TestCase):
    def test_aggregate(self):
        with open(f"{fixtures_path}/impact-assessment/countries/aggregated.jsonld", encoding='utf-8') as f:
            impacts = json.load(f)
        with open(f"{fixtures_path}/impact-assessment/world/aggregated.jsonld", encoding='utf-8') as f:
            expected = json.load(f)
        impacts_by_product = _group_impacts_by_product(impacts, False)
        results = aggregate(impacts_by_product)
        results = list(map(_update_impact_assessment({'@id': 'region-world'}), results))
        self.assertEqual(results, expected)
        self.assertEqual(len(results), 6)
