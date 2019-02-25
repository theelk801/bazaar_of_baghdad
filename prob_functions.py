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


@functools.lru_cache(maxsize=None)
def prob_of_keep(bazaars_in_hand, powders_in_hand, other_in_hand, bazaars_in_deck, powders_in_deck, other_in_deck,
                 mull_count=0):
    if bazaars_in_hand > 0:
        return 1.0
    if mull_count > 5:
        return 0.0

    # start with regular mulligan odds
    regular_mull = 0
    for i, j, k in hand_gen(bazaars_in_deck, powders_in_deck, other_in_deck):
        prob = hypogeo(bazaars_in_deck, i, powders_in_deck, j, other_in_deck, k)
        # print(prob)
        prob *= prob_of_keep(i, j, k, bazaars_in_deck, powders_in_deck, other_in_deck, mull_count + 1)
        # print(prob)
        regular_mull += prob

    # if serum powder not in hand, or probability is already 1, we can stop
    if powders_in_hand == 0 or regular_mull == 1.0:
        return regular_mull

    # create list of all possible outcomes
    all_mulls = [regular_mull]
    for powders_on_bottom, other_on_bottom in powder_gen(powders_in_hand, other_in_hand, mull_count):
        powders_left = powders_in_deck - powders_in_hand + powders_on_bottom
        other_left = other_in_deck - other_in_hand + other_on_bottom
        powder_mull = 0
        for i, j, k in hand_gen(bazaars_in_deck, powders_left, other_left):
            prob = hypogeo(bazaars_in_deck, i, powders_left, j, other_left, k)
            prob *= prob_of_keep(i, j, k, bazaars_in_deck, powders_left, other_left, mull_count)
            powder_mull += prob
        if powder_mull == 1.0:
            return 1.0
        all_mulls.append(powder_mull)
    return max(all_mulls)


def prob_of_good_hand(bazaars=4, powders=4, other=52):
    total = 0
    for i, j, k in hand_gen(bazaars, powders, other):
        prob = hypogeo(bazaars, i, powders, j, other, k)
        prob *= prob_of_keep(i, j, k, bazaars, powders, other)
        total += prob
    return total


def advice_string(key):
    if key == 'regular':
        print('Take a regular mulligan.')
        return
    a, b = key
    print(f'Put {a} Serum Powder and {b} other card' + ('s' if b != 1 else '') + ' on the bottom.')


def action_to_take(powders_in_hand, other_in_hand, powders_in_deck, other_in_deck, mull_count):
    mull_dict = dict()
    regular_mull = 0
    for i, j, k in hand_gen(4, powders_in_deck, other_in_deck):
        prob = hypogeo(4, i, powders_in_deck, j, other_in_deck, k)
        # print(prob)
        prob *= prob_of_keep(i, j, k, 4, powders_in_deck, other_in_deck, mull_count + 1)
        # print(prob)
        regular_mull += prob
    mull_dict['regular'] = regular_mull

    for powders_on_bottom, other_on_bottom in powder_gen(powders_in_hand, other_in_hand, mull_count):
        powders_left = powders_in_deck - powders_in_hand + powders_on_bottom
        other_left = other_in_deck - other_in_hand + other_on_bottom
        powder_mull = 0
        for i, j, k in hand_gen(4, powders_left, other_left):
            prob = hypogeo(4, i, powders_left, j, other_left, k)
            prob *= prob_of_keep(i, j, k, 4, powders_left, other_left, mull_count)
            powder_mull += prob
        mull_dict[(powders_on_bottom, other_on_bottom)] = powder_mull

    m = max(mull_dict.keys(), key=lambda x: mull_dict[x])
    print(advice_string(m))
