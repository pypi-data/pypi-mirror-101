import unittest
from unittest.mock import patch
from pathlib import Path
import json
import statistics

from quantifin.util.greeks import *


class TestCase(unittest.TestCase):
    def setUp(self):
        self.base_path = Path(__file__).parent
        self.price_dict = {'2020-01-01': 2008.719970703125,'2020-02-01': 1883.75,'2020-03-01': 1949.719970703125,'2020-04-01': 2474.0,'2020-05-01': 2442.3701171875,'2020-06-01': 2758.820068359375,
                            '2020-07-01': 3164.679931640625,'2020-08-01': 3450.9599609375,'2020-09-01': 3148.72998046875,'2020-10-01': 3036.14990234375,'2020-11-01': 3168.0400390625,'2020-12-01': 3256.929931640625}
        self.sample_return = [-0.06, 0.2, -0.1, 0.24, -0.14, 0.2, 0.2, 0.16, 0.14]
        self.period_benchmark =  [0.02, 0.03, 0.026, 0.01, 0.022, 0.022, 0.01, 0.04, 0.01]
    
    def test_calculate_differential_return(self):
        self.assertRaises(ValueError, calculate_differential_returns, self.sample_return, self.period_benchmark[:-1])
        correct_result = [0.08, 0.17, 0.126, 0.23, 0.162, 0.178, 0.19, 0.12, 0.13]
        self.assertEqual(calculate_differential_returns(self.sample_return, self.period_benchmark, absolute=True), correct_result)
        self.assertEqual(calculate_differential_returns(self.sample_return, self.period_benchmark, absolute=False), [-0.08, 0.17, -0.126, 0.23, -0.162, 0.178, 0.19, 0.12, 0.13])

    def test_sharpe_ratio_ex_post(self):
        returns = price_returns(self.price_dict)
        benchmark = [0.02 for i in range(len(self.sample_return))]
        self.assertEqual(sharpe_ratio_ex_post(self.sample_return, benchmark), 3.6141)
        self.assertEqual(sharpe_ratio_ex_post(returns, [0.005 for i in range(len(returns))]), 1.1588)
    
    def test_sharpe_ratio_ex_ante(self):
        self.assertEqual(sharpe_ratio_ex_ante(0.1, 0.03, 0.16), 0.43750)

    def test_sortino_ratio(self):
        return_rates = [0.17, 0.15, 0.23, -0.05, 0.12, 0.09, 0.13, -0.04]
        self.assertRaises(ValueError, sortino_ratio, self.sample_return, self.period_benchmark[:-1])
        self.assertEqual(sortino_ratio(return_rates, [0 for i in range(len(return_rates))]), 4.417)
        self.assertEqual(sortino_ratio(return_rates, [0.03 for i in range(len(return_rates))]), 1.863)
    
    def test_alpha(self):
        self.assertEqual(alpha(0.1, 0.08, 0.03, 1.2), 0.01) 
    
def read_price_list(path):
    with open(path, "r") as r:
        return json.load(r)
