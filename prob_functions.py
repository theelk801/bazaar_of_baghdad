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
    for i in range(bazaars + 1):
        for j in range(powders + 1):
            for k in range(other + 1):
                if i + j + k == hand_size:
                    yield i, j, k


def powder_gen(powders_in_hand, other_in_hand, to_put_under):
    for i in range(powders_in_hand):
        for j in range(other_in_hand + 1):
            if i + j == to_put_under:
                yield i, j

#     return max(regular_mull(powders, other), powder_mull(powders, other))
