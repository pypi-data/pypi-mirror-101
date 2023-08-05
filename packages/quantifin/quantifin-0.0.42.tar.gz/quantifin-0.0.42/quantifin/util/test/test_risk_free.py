
import unittest
from unittest.mock import patch
from pathlib import Path
from json import load

from quantifin.util import RiskFree


class TestCase(unittest.TestCase):
    def setUp(self):
        self.base_path = Path(__file__).parent
        self.ten_year = RiskFree(10)
    
    def read_json(self, file_path):
        with open (file_path) as f:
            json_dict = load(f)
        return json_dict

    def test_mapping(self):
        ten_year = RiskFree(10)
        self.assertEqual(ten_year.market_code, "^TNX")
        thirty_year = RiskFree(30)
        self.assertEqual(thirty_year.market_code, "^TYX")
        five_year = RiskFree(5)
        self.assertEqual(five_year.market_code, "^FVX")
        self.assertRaises(KeyError, RiskFree, 3)

    @patch.object(RiskFree, "get_prev_close_price", return_value = 1.52)
    def test_spot_yield(self, MockPrevPrice):
        self.assertEqual(self.ten_year.spot_yield, 0.0152)
        self.assertTrue(MockPrevPrice.called)
    
    @patch.object(RiskFree, "get_prev_close_price", return_value = None)
    def test_spot_yield_none(self, MockPrevPrice):
        self.assertEqual(self.ten_year.spot_yield, None)

    @patch.object(RiskFree, 'get_historical_price_data')
    def test_yield_history(self, MockHistPrice):
        MockHistPrice.side_effect = lambda start, end, period: self.read_json(str(self.base_path) + '/resource/historical_yield.json')
        correct = [0.009, 0.008, 0.009, 0.007, 0.007, 0.005, 0.007, 0.006, 0.006, 0.007, 0.011, 0.015] #Ensure descending time order from latest to oldest 
        self.assertEqual(self.ten_year.yield_history("2020-01-01", "2021-01-01", "monthly"), correct)