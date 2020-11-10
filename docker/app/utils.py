import scipy.stats as stats

def is_probability_distribution(x, is_continuous=True):
    parent = stats.rv_continuous if is_continuous else stats.rv_discreate
    try:
        return issubclass(type(x), parent)
    except TypeError as e:
        return False


def is_continuous(x):
    return is_probability_distribution(x, is_continuous=True)


def is_discreate(x):
    return is_probability_distribution(x, is_continuous=False)
