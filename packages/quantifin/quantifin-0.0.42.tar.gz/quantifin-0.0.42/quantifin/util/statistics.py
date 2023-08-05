from scipy.stats import describe
def coefficient_of_variation(iterable):
    return round(describe(iterable).variance ** 0.5 / describe(iterable).mean, 4)