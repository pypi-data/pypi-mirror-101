import unittest
from unittest.mock import patch, MagicMock, PropertyMock
from pathlib import Path
from json import load
import yahoofinancials as yf
from datetime import datetime

from quantifin.equity import Stock
from quantifin.equity.valuation import *
from quantifin.util import markets, RiskFree

yield_history  = [0.009,0.008,0.009,0.007,0.007,0.005,0.007,0.006,0.006,0.007,0.011,0.015]

@patch.object(Stock, 'get_beta', return_value = 2.2)
class TestCase(unittest.TestCase):
    def setUp(self):
        self.base_path = Path(__file__).parent
        self.index_json = self.read_json(str(self.base_path) + "/resource/market_price.json")
    
    def read_json(self, file_path):
        with open (file_path) as f:
            json_dict = load(f)
        return json_dict

    def test_CAPM(self, MockGetBeta):
        req_rate_CAPM = CAPM(0.02, 0.1, 1.2)
        self.assertEqual(req_rate_CAPM, 0.116)
    
    #################
    #Dividend testing
    #################
    def test_get_FY_dividend_period(self, MockGetBeta):
        stock = Stock("AAPL")
        dec = datetime(2019, 12, 10)
        self.assertEqual(stock._get_FY_dividend_period(dec), [datetime(2019, 1, 1), dec])

        not_dec = datetime(2019, 11, 29)
        self.assertEqual(stock._get_FY_dividend_period(not_dec), [datetime(2018, 1, 1), datetime(2018, 12, 30)])
    

    def test_calculate_dividend(self, MockGetBeta):
        stock = Stock("D05.SI")

        dividend_resp = self.read_json(str(self.base_path) + "/resource/dividend/2020_dbs_dividend.json")
        
        self.assertEqual(stock._calculate_full_dividend(dividend_resp), 1.35)
        self.assertEqual(stock._calculate_full_dividend({"D05.SI": None}), 0)
        amzn = Stock("AMZN")
        dividend_resp = {'AMZN': None}
        self.assertEqual(amzn._calculate_full_dividend(dividend_resp), 0)

    @patch.object(Stock, 'get_daily_dividend_data')
    def test_get_current_dividend(self, MockDividend, MockGetBeta):
            
        MockDividend.side_effect = self.get_dividend_side_effect
        stock = Stock("D05.SI")
        self.assertEqual(stock.full_year_dividend(), 1.35)
    
    def get_dividend_side_effect(self, start_date, end_date):
        dividend_path = str(self.base_path) + "/resource/dividend/2020_dbs_dividend.json"
        return self.read_json(dividend_path)

    #Payout Ratio tests
    @patch.object(Stock, 'get_financial_stmts')
    def test_average_payout_ratio(self, MockGetFnStmts, MockGetBeta):
        MockGetFnStmts.side_effect = self.get_financial_stmts_side_effect
        stock = Stock("D05.SI")
        cf = stock.get_financial_stmts('annual', 'cash')
        correct = {'2020': 0.511, '2019': 0.615, '2018': 0.565, '2017': 0.315}
        self.assertEqual(stock.get_dividend_payout_ratio_history(), correct)
        self.assertEqual(stock.average_dividend_payout_ratio(stock.get_dividend_payout_ratio_history()), 0.501)
    
    @patch.object(Stock, 'get_financial_stmts')
    def test_payout_history_no_payout(self, MockCashFlow, MockGetBeta):
        MockCashFlow.side_effect = lambda p, s: self.read_json(str(self.base_path) + '/resource/financial_statements/AMZN_cash_flow_stmts.json')
        amzn = Stock("AMZN")
        self.assertEqual(amzn.get_dividend_payout_ratio_history(), {'2020': 0, "2019": 0, "2018": 0, "2017": 0})
    
    @patch.object(Stock, "get_financial_stmts")
    def test_get_roe_history(self, MockGetFnStmts, MockGetBeta):
        MockGetFnStmts.side_effect = self.get_financial_stmts_side_effect

        stock = Stock("D05.SI")
        correct_result = {"2020": 0.086, "2019": 0.123, "2018": 0.112, "2017": 0.088}
        self.assertEqual(stock.get_roe_history(), correct_result)
    
    def test_calulate_roe(self, MockGetBeta):
        stock = Stock("D05.SI")
        self.assertRaises(ValueError, stock.calculate_roe, 100, 0)
        self.assertRaises(ValueError, stock.calculate_roe, 100, -100)
        self.assertEqual(stock.calculate_roe(50, 300), 0.167)
    
    @patch.object(Stock, "get_financial_stmts")
    def test_get_average_roe(self, MockGetFnStmts, MockGetBeta):
        MockGetFnStmts.side_effect = self.get_financial_stmts_side_effect
        stock = Stock("D05.SI")
        roe = stock.get_roe_history()
        self.assertEqual(stock.average_roe(roe), 0.102)

    @patch.object(Stock, "get_financial_stmts")
    def test_growth_rate(self, MockGetFnStmts, MockGetBeta):
        MockGetFnStmts.side_effect = self.get_financial_stmts_side_effect
        stock = Stock("D05.SI")
        self.assertEqual(stock.growth_rate(), 0.051)
    
    ####################
    #Test Free Cash Flow
    ####################
    @patch.object(Stock, "get_financial_stmts")
    def test_fcf_history(self, MockGetFnStmts, MockGetBeta):
        MockGetFnStmts.side_effect = lambda p, s: self.read_json(str(self.base_path) + '/resource/financial_statements/AMZN_cash_flow_stmts.json')
        stock = Stock("AMZN")
        correct_result = {"2020": 25924000000, "2019": 21653000000 , "2018": 17296000000, "2017": 6410000000}
        self.assertEqual(stock.get_fcf_history(), correct_result)
    
    @patch.object(Stock, "get_fcf_history", return_value = {"2020": 1000, "2019": 800, "2018": 600,"2017": 500})
    def test_fcf_growth_rate(self, MockFCFHistory, MockGetBeta):
        stock = Stock("D05.SI")
        self.assertEqual(stock.fcf_growth_rate(), 0.261)
        self.assertTrue(MockFCFHistory.called)

    #########################
    #Test Statistics & Greeks
    #########################
    @patch.object(Stock, "get_historical_price_data")
    @patch.object(RiskFree, "yield_history", return_value = yield_history)
    def test_sharpe_ratio(self, MockYieldHistory, MockHistPrice, MockGetBeta):
        MockHistPrice.side_effect = lambda start, end, period: self.read_json(str(self.base_path) + '/resource/historical_price.json')
        s = Stock("AMZN")

        self.assertEqual(s.get_sharpe_ratio_ex_post("2020-01-01", "2021-01-01", "monthly", yield_history[1:]), 1.15593)
        self.assertFalse(MockYieldHistory.called)
        self.assertEqual(s.get_sharpe_ratio_ex_post("2020-01-01", "2021-01-01", "monthly"), 1.15593)
        self.assertTrue(MockYieldHistory.called)
    
    @patch.object(Stock, "get_historical_price_data")
    @patch.object(RiskFree, "yield_history", return_value = yield_history)
    def test_sortino_ratio(self, MockYieldHistory,MockHistPrice, MockGetBeta):
        MockHistPrice.side_effect = lambda start, end, period: self.read_json(str(self.base_path) + '/resource/historical_price.json')
        s = Stock("AMZN")
        benchmark_rates = yield_history[1:]

        self.assertEqual(s.get_sortino_ratio("2020-01-01", "2021-01-01", "monthly", benchmark_rates), 1.047)
        self.assertEqual(s.get_sortino_ratio("2020-01-01", "2021-01-01", "monthly"), 1.047)

    @patch.object(Stock, "get_historical_price_data")
    def test_coeff_variation(self, MockHistPrice, MockGetBeta):
        MockHistPrice.side_effect =  lambda start, end, period: self.read_json(str(self.base_path) + '/resource/historical_price.json')
        s = Stock("AMZN")
        self.assertEqual(s.get_coefficient_of_variation(5, "weekly"), 2.109)
    
    @patch.object(Stock, "get_historical_price_data")
    def test_alpha(self, MockHistPrice, MockGetBeta):
        MockHistPrice.side_effect =  lambda start, end, period: self.read_json(str(self.base_path) + '/resource/historical_price.json')
        s = Stock("AMZN")
        self.assertEqual(s.get_alpha(3, 0.1, 0.03), 0.437)
    
    @patch.object(Stock, 'get_key_statistics_data')
    @patch.object(Stock, "get_financial_stmts")
    def test_ebitda_related(self, MockGetFnStmts, MockKeyStats, MockGetBeta):
        MockKeyStats.side_effect =  lambda: self.read_json(str(self.base_path) + '/resource/key_statistics.json')
        MockGetFnStmts.side_effect = self.get_financial_stmts_side_effect
        stock = Stock("D05.SI")
        self.assertEqual(stock.ebitda, 6016000000)
        self.assertEqual(stock.enterprise_to_ebitda(), 17.573)

        with patch("quantifin.equity.Stock.key_stats", new_callable=PropertyMock) as mock_key_stats:
            mock_key_stats.return_value = {"enterpriseToEbitda": 15.123}
            stock = Stock("D05.SI")
            self.assertEqual(stock.enterprise_to_ebitda(), 15.123)
        
    @patch.object(Stock, 'get_key_statistics_data')
    @patch.object(Stock, "get_fcf_history", return_value = {"2020": 25924000000, "2019": 21653000000 , "2018": 17296000000, "2017": 6410000000})
    def test_enterprise_value_fcf(self, MockFCFHistory,MockKeyStats, MockGetBeta):
        MockKeyStats.side_effect =  lambda: self.read_json(str(self.base_path) + '/resource/key_statistics.json')
        stock = Stock("D05.SI")
        self.assertEqual(stock.enterprise_to_fcf(), 4.078)


    def get_financial_stmts_side_effect(self, period, stmt_type):
        if( stmt_type == "cash"):
            return(self.read_json(str(self.base_path) + '/resource/financial_statements/cash_flow_stmts.json'))
        if(stmt_type == "income"):
            return(self.read_json(str(self.base_path) + '/resource/financial_statements/income_stmts.json'))
        if(stmt_type == "balance"):
            return(self.read_json(str(self.base_path) + '/resource/financial_statements/balance_sheet_stmts.json'))
