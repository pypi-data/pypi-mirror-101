import yahoofinancials as yf
import datetime
from functools import partial
from quantifin.util.greeks import *
from quantifin.util import statistics
from quantifin.util import RiskFree, extract_prices 
from scipy.stats import kurtosis, skew

class Stock(yf.YahooFinancials):
    def __init__(self, stock_code):
        self.stock_code = stock_code
        super().__init__(stock_code)
        self.__beta = None 
        self.__cash_flow = None
        self.__income = None
        self.__balance_sheets = None
        self.__key_stats = None

    @staticmethod
    def get_date_key(input_dict: dict):
        return (list(input_dict.keys())[0])

    @property
    def beta(self):
        if self.__beta == None:
            self.__beta = self.get_beta() if self.get_beta() else 1
        return self.__beta
    
    @property
    def trailing_eps(self):
        try:
            return self.key_stats['trailingEps']
        except KeyError:
            return None 
    
    @property
    def forward_eps(self):
        try:
            return self.key_stats['forwardEps']
        except KeyError:
            return None

    @property
    def key_stats(self):
        if self.__key_stats is None:
            self.__key_stats = self.get_key_statistics_data()[self.stock_code]
        return self.__key_stats

    @property
    def cash_flow_stmts(self):
        if self.__cash_flow == None:
            self.__cash_flow =  self.get_financial_stmts("annual", "cash")['cashflowStatementHistory'][self.stock_code]
        return self.__cash_flow
    
    @property
    def income_stmts(self):
        if self.__income == None:
            self.__income = self.get_financial_stmts("annual", "income")['incomeStatementHistory'][self.stock_code]
        return self.__income
    
    @property
    def balance_sheet_stmts(self):
        if self.__balance_sheets == None:
            self.__balance_sheets = self.get_financial_stmts("annual", "balance")['balanceSheetHistory'][self.stock_code]
        return self.__balance_sheets

    @property
    def enterprise_value(self):
        try:
            return self.key_stats['enterpriseValue']
        except KeyError:
            return None
    @property
    def ebitda(self):
        try:
            date_key = Stock.get_date_key(self.income_stmts[0])
            return self.income_stmts[0].get(date_key).get("operatingIncome") + self.cash_flow_stmts[0].get(date_key).get("depreciation")
        except KeyError:
            return None    

    def full_year_dividend(self):
        now_date = datetime.datetime.now()
        start_of_year, end_of_year = self._get_FY_dividend_period(now_date)
        dividend_resp = self.get_daily_dividend_data(start_of_year.strftime("%Y-%m-%d"), end_of_year.strftime("%Y-%m-%d"))
        return self._calculate_full_dividend(dividend_resp)
    
    def _get_FY_dividend_period(self, now: datetime.datetime):
        def current_year(now: datetime.datetime):
            this_year = now.year
            return [datetime.datetime(this_year, 1, 1), now]
        
        def previous_year(now: datetime.datetime):
            year = now.year - 1
            return [datetime.datetime(year, 1, 1), datetime.datetime(year, 12, 30)]

        if (now.month == 12):
            return current_year(now) 
        return previous_year(now)
    

    def _calculate_full_dividend(self, dividend_resp: dict):
        if dividend_resp[self.stock_code] is None:
            return 0
        dividends = [payout['amount'] for payout in dividend_resp[self.stock_code]]
        return round(sum(dividends), 3)

    def get_dividend_payout_ratio_history(self):
        ###Helper functions
        
        def calculate_payout(cash_flow):
            try:
                div_payout = abs(int(cash_flow['dividendsPaid']))
            except KeyError:
                return 0
            net_income = int(cash_flow['netIncome'])
            if net_income < 0:
                return 0
            return round(div_payout/net_income, 3)

        def get_payout_ratios(cf_stmts_list):
            result = {}
            for cash_flow in self.cash_flow_stmts:
                date_key = Stock.get_date_key(cash_flow)
                result[date_key[:4]] = calculate_payout(cash_flow[date_key])
            return result
        ## End of helper functions
        return get_payout_ratios(self.cash_flow_stmts)
    
    def average_dividend_payout_ratio(self, payout_ratio_history: dict):
        payout_list = [payout for payout in payout_ratio_history.values()]
        return round(sum(payout_list) / len(payout_list), 3)
    
    def get_roe_history(self):
        result = {}
        for i in range(len(self.balance_sheet_stmts)):
            date_key = Stock.get_date_key(self.balance_sheet_stmts[i])
            net_equity = self.balance_sheet_stmts[i][date_key]['totalAssets'] - self.balance_sheet_stmts[i][date_key]['totalLiab']
            net_income = self.income_stmts[i][date_key]['netIncome']
            result[date_key[:4]] = self.calculate_roe(net_income, net_equity)
        return result

    def calculate_roe(self, income: float, equity: float):
        if equity == 0:
            raise ValueError("Equity should be a non-zero value. 0 was passed as equity")
        if equity < 0:
            raise ValueError(f"Equity is negative: {equity}. A postive value should be passed in")
        return round(income/equity, 3)

    def average_roe(self, roe_history: dict):
        sum = 0
        for roe in roe_history.values():
            sum += roe
        return round(sum / len(roe_history), 3)
    
    def growth_rate(self):
        payout = self.average_dividend_payout_ratio(self.get_dividend_payout_ratio_history())
        roe = self.average_roe(self.get_roe_history())
        if payout > 1:
            raise ValueError("Payout rate exceeds 1. Invalid value for growth rate")
        if roe < 0:
            raise ValueError("ROE is negative. Invalid value for growth rate")
        return round((1 - payout) * roe, 3)

    def get_fcf_history(self):
        def calculate_net_fcf(cf_stmt):
            p_extract_key  =partial(extract_key, cf_stmt)
            operating = p_extract_key('totalCashFromOperatingActivities')
            capex = p_extract_key("capitalExpenditures")
            return operating + capex

        def extract_key(cf,key):
            try:
                return cf[key]
            except KeyError:
                return 0

        cf_history = {}
        for period in self.cash_flow_stmts:
            date_key = Stock.get_date_key(period)
            cf_history[date_key[:4]] = calculate_net_fcf(period[date_key])
        return cf_history
    
    def fcf_growth_rate(self):
        fcf_history = [i for i in self.get_fcf_history().values()]
        growth_comparator = list(zip(fcf_history, fcf_history[1:]))
        cummulative_growth = 0
        for comp in growth_comparator:
            cummulative_growth += (comp[0] / comp[1])
        return round(((cummulative_growth / len(growth_comparator)) - 1), 3)
    
    def get_sharpe_ratio_ex_post(self, start_date, end_date, period, benchmark_rate = None):
        if benchmark_rate is None:
            benchmark_rate = self.__default_benchmark(start_date, end_date, period)
        differential_return = self.__get_diff_returns(start_date, end_date, period)
        return sharpe_ratio_ex_post(differential_return, benchmark_rate)
    
    def __default_benchmark(self, start, end, period):
        yields = RiskFree(10).yield_history(start, end, period)[1:] #drop current spot yield
        return yields
    
    def __get_diff_returns(self, start_date, end_date, period):
        prices = extract_prices(self.get_historical_price_data(start_date, end_date, period), self.stock_code)
        return price_returns(prices)

    def get_sortino_ratio(self, start_date, end_date, period, benchmark_rate = None):
        if benchmark_rate is None:
            benchmark_rate = self.__default_benchmark(start_date, end_date, period)
        differential_return = self.__get_diff_returns(start_date, end_date, period)
        return sortino_ratio(differential_return, benchmark_rate)
    
    def get_coefficient_of_variation(self, years, period):
        today = self.__get_today()
        start_date = datetime.datetime(today.year - years, today.month, today.day)
        stock_returns = self.__get_diff_returns(start_date.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d"), period)
        return(statistics.coefficient_of_variation(stock_returns))

    def get_alpha(self, years, market_return, risk_free):
        today = self.__get_today()
        start_date = datetime.datetime(today.year - years, today.month, today.day)
        price_list = extract_prices(self.get_historical_price_data(start_date.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d"), "monthly"), self.stock_code)
        sorted_period_key = sorted(price_list, reverse=True)        #Extra step for testability using mock
        period_return = (price_list.get(sorted_period_key[0]) / price_list.get(sorted_period_key[-1])) - 1
        return alpha(period_return, market_return, risk_free, self.beta)

    def __get_today(self):
        today = datetime.datetime.now()
        if today.day == 1:
            today - datetime.timedelta(days = 1)
        return today
    def enterprise_to_ebitda(self):
        try:
            ev_ebitda = self.key_stats["enterpriseToEbitda"]
        except KeyError:
            return None
        if ev_ebitda is not None:
            return ev_ebitda
        return round(self.enterprise_value / self.ebitda, 3)
    
    def enterprise_to_fcf(self):
        fcf_history = self.get_fcf_history()
        latest_fcf = fcf_history.get(sorted(fcf_history.keys())[-1])
        return round(self.enterprise_value / latest_fcf, 3)
         