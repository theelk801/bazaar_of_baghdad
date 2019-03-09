from functools import lru_cache
from math import factorial as fac


@lru_cache(maxsize=None)
def bino(a, b):
    """
    computes the binomial coefficient (a choose b)
    """
    if b > a:
        return 0
    return fac(a) // (fac(a - b) * fac(b))


@lru_cache(maxsize=None)
def hypogeo(N1, n1, N2, n2, N3, n3):
    """
    computes hypergeometric probability in three variables
    """
    numerator = bino(N1, n1) * bino(N2, n2) * bino(N3, n3)
    denominator = bino(N1 + N2 + N3, n1 + n2 + n3)
    return numerator / denominator


def hand_gen(bazaars, powders, other, hand_size=7):
    """
    generates all possible opening hands given makeup of the deck
    """
    for i in range(bazaars + 1):
        for j in range(powders + 1):
            for k in range(other + 1):
                if i + j + k == hand_size:
                    yield i, j, k


def powder_gen(powders_in_hand, other_in_hand, to_put_under):
    """
    generates all possible ways to put cards from hand onto bottom of library while mulling, leaving at least one powder
    assumes that there are no bazaar in hand as the hand would be kept
    """
    for i in range(powders_in_hand):
        for j in range(other_in_hand + 1):
            if i + j == to_put_under:
                yield i, j


@lru_cache(maxsize=None)
def prob_of_keep(bazaars_in_hand,
                 bazaars_in_deck,
                 powders_in_hand,
                 powders_in_deck,
                 other_in_hand,
                 other_in_deck,
                 powders_on_bottom=0,
                 other_on_bottom=0,
                 mull_count=0):
    """
    computes the probability that a given hand will result in a keep or will mulligan into a hand that will keep
    """

    # make sure that we're never trying to draw from a library which is too small
    if bazaars_in_deck + powders_in_deck + other_in_deck < 7:
        raise Exception('Not enough cards in library')

    # start with easy pass/fails
    if bazaars_in_hand > 0:
        return 1.0
    if mull_count > 6:
        return 0.0

    # start with regular mulligan odds
    regular_mull = 0
    for i, j, k in hand_gen(bazaars_in_deck,
                            powders_in_deck + powders_on_bottom,
                            other_in_deck + other_on_bottom):
        # find probability of hand being drawn
        prob = hypogeo(bazaars_in_deck, i, powders_in_deck + powders_on_bottom,
                       j, other_in_deck + other_on_bottom, k)
        # multiply by probability of hand leading to a keep
        prob *= prob_of_keep(
            i,
            bazaars_in_deck,
            j,
            powders_in_deck + powders_on_bottom,
            k,
            other_in_deck + other_on_bottom,
            mull_count=mull_count + 1)
        regular_mull += prob

    # if serum powder not in hand, or probability is already 1, we can stop
    if powders_in_hand == 0 or regular_mull == 1.0:
        return regular_mull

    # create list of all possible outcomes
    all_mulls = [regular_mull]

    # iterate over all possible ways to put cards on the bottom
    for powders_to_bottom, other_to_bottom in powder_gen(
            powders_in_hand, other_in_hand, mull_count):
        powders_left = powders_in_deck - powders_in_hand
        other_left = other_in_deck - other_in_hand
        powder_mull = 0
        for i, j, k in hand_gen(bazaars_in_deck, powders_left, other_left,
                                7 - mull_count):
            prob = hypogeo(bazaars_in_deck, i, powders_left, j, other_left, k)
            prob *= prob_of_keep(i, bazaars_in_deck, j, powders_left, k,
                                 other_left,
                                 powders_on_bottom + powders_to_bottom,
                                 other_on_bottom + other_to_bottom, mull_count)
            powder_mull += prob
        if powder_mull == 1.0:
            return 1.0
        all_mulls.append(powder_mull)
    return max(all_mulls)


def prob_of_good_hand(bazaars=4, powders=4, other=52):
    """
    computes the overall probability of a keep for all possible hands
    """
    total = 0
    for i, j, k in hand_gen(bazaars, powders, other):
        prob = hypogeo(bazaars, i, powders, j, other, k)
        prob *= prob_of_keep(i, bazaars, j, powders, k, other)
        total += prob
    return total


def advice_string(key, mull_count):
    """
    parses the mulligan decision into a readable string
    """
    if key == 'regular':
        return 'Take a regular mulligan.'
    if mull_count == 0:
        return 'Use Serum Powder.'
    a, b = key
    return f'Put {a} Serum Powder and {b} other card' + (
        's' if b != 1 else '') + ' on the bottom then use Serum Powder.'


def action_to_take(powders_in_hand,
                   other_in_hand,
                   powders_in_deck,
                   other_in_deck,
                   powders_on_bottom=0,
                   other_on_bottom=0,
                   mull_count=0):
    """
    given a hand, advises on how to proceed
    """
    mull_dict = dict()
    regular_mull = 0
    for i, j, k in hand_gen(4, powders_in_deck + powders_on_bottom,
                            other_in_deck + other_on_bottom):
        prob = hypogeo(4, i, powders_in_deck + powders_on_bottom, j,
                       other_in_deck + other_on_bottom, k)
        prob *= prob_of_keep(
            i,
            4,
            j,
            powders_in_deck + powders_on_bottom,
            k,
            other_in_deck + other_on_bottom,
            mull_count=mull_count + 1)
        regular_mull += prob
    mull_dict['regular'] = regular_mull

    for powders_to_bottom, other_to_bottom in powder_gen(
            powders_in_hand, other_in_hand, mull_count):
        powders_left = powders_in_deck - powders_in_hand
        other_left = other_in_deck - other_in_hand
        powder_mull = 0
        for i, j, k in hand_gen(4, powders_left, other_left, 7 - mull_count):
            prob = hypogeo(4, i, powders_left, j, other_left, k)
            prob *= prob_of_keep(i, 4, j, powders_left, k, other_left,
                                 powders_on_bottom + powders_to_bottom,
                                 other_on_bottom + other_to_bottom, mull_count)
            powder_mull += prob
        mull_dict[(powders_to_bottom, other_to_bottom)] = powder_mull

    best_action = max(mull_dict.keys(), key=mull_dict.get)
    return best_action
