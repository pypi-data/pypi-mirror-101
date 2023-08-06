import unittest
from unittest.mock import patch
import json

from tests.utils import fixtures_path, fake_grouped_impacts
from hestia_earth.aggregation.models.terms import aggregate
from hestia_earth.aggregation.impact_assessment_utils import _update_impact_assessment

class_path = 'hestia_earth.aggregation.models.terms'

with open(f"{fixtures_path}/terms.jsonld", encoding='utf-8') as f:
    terms = json.load(f)


class TestTerms(unittest.TestCase):
    @patch(f"{class_path}._all_terms", return_value=terms)
    def test_aggregate(self, _m):
        with open(f"{fixtures_path}/impact-assessment/terms/aggregated.jsonld", encoding='utf-8') as f:
            expected = json.load(f)
        impacts = fake_grouped_impacts()
        results = aggregate(impacts)
        results = list(map(lambda result: _update_impact_assessment(result['country'])(result), results))
        self.assertEqual(results, expected)
        self.assertEqual(len(results), 11)
