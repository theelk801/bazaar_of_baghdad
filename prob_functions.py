import functools
from math import factorial as fac


@functools.lru_cache(maxsize=None)
def bino(a, b):
    if b > a:
        return 0
    return fac(a) // (fac(a - b) * fac(b))


@functools.lru_cache(maxsize=None)
def hypogeo(N1, n1, N2, n2, N3, n3):
    numerator = bino(N1, n1) * bino(N2, n2) * bino(N3, n3)
    denominator = bino(N1 + N2 + N3, n1 + n2 + n3)
    return numerator / denominator


def hand_gen(bazaars, powders, other, hand_size=7):
    for i in range(bazaars):
        for j in range(powders):
            for k in range(other):
                if i + j + k == hand_size:
                    yield i, j, k

