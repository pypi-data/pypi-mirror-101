from statistics import stdev
from functools import reduce
from math import sqrt
from .helper import price_returns

# def price_returns(price_list):
#     combined_price = zip(price_list, price_list[1:])
#     returns = []
#     for i in combined_price:
#         returns.append((i[0] / i[1]) - 1)
#     return returns


def sharpe_ratio_ex_ante(expected_return, benchmark_rate, sigma):
    '''Predicting future sharpe ratio'''
    return round((expected_return - benchmark_rate) / sigma, 5)


def sharpe_ratio_ex_post(returns_list, benchmark_list):
    differential_return = calculate_differential_returns(returns_list, benchmark_list, absolute=True)
    sigma = stdev(differential_return)
    return round(__average(differential_return) / sigma, 5)

def calculate_differential_returns(returns, benchmark, absolute = False):
    __assert_rates_tally(returns, benchmark)
    zipped = zip(returns, benchmark)
    return [__calculate_differential_return(pair[0], pair[1], absolute) for pair in zipped]

def __assert_rates_tally(returns, benchmark):
    if len(returns) != len(benchmark):
        raise ValueError(f"Number of returns: {len(returns)} provided does not correspond to benchmark rates provided: {len(benchmark)}")

def __calculate_differential_return(returns, benchmark, absolute = False):
    if absolute:
        return round(abs(returns - benchmark), 3)
    return round(returns - benchmark, 3)

def __average(iterable):
    return sum(iterable) / len(iterable)

def sortino_ratio(returns_list, benchmark):
    __assert_rates_tally(returns_list, benchmark)
    differential_returns = calculate_differential_returns(returns_list, benchmark, absolute=False)
    avg_return = __average(differential_returns)
    downside_deviation = __calculate_downside_deviation(differential_returns)
    return round(avg_return / downside_deviation, 3)

def __calculate_downside_deviation(diff_return):
    downside_deviation_list = [abs((re) ** 2) for re in diff_return if re < 0]
    return sqrt(sum(downside_deviation_list)/ len(diff_return))

def alpha(realised_return, market_return, risk_free, beta):
    return round(realised_return - (risk_free + ((market_return - risk_free) * beta)), 3)