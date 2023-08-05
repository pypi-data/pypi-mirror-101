import unittest
from unittest.mock import patch
from pathlib import Path
import json
import scipy.stats

from quantifin.util.statistics import *

class TestCase(unittest.TestCase):
    def setUp(self):
        self.base_path = Path(__file__).parent
        self.test_return = [10, 30, 20, 23]
    
    def test_coefficient_of_variation(self):
        self.assertEqual(coefficient_of_variation(self.test_return),0.4001)
        

