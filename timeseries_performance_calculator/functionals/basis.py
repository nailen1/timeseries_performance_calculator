from functools import reduce

def pipe(*functions):
    return lambda x: reduce(lambda acc, f: f(acc), functions, x)
