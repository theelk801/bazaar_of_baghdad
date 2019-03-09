from prob_functions import *


def get_input(prompt):
    while True:
        try:
            return int(input(prompt + '\n'))
        except (ValueError, NameError):
            print('Please enter a number')


powders_in_deck = 4
other_in_deck = 52
powders_on_bottom = 0
other_on_bottom = 0
mull_count = 0

while True:
    print('\nIf you have a Bazaar, keep!\n')

    powders_in_hand = get_input('How many Serum Powder are in your hand?')
    other_in_hand = get_input('How many other cards are in your hand?')

    best_action = action_to_take(powders_in_hand, other_in_hand, powders_in_deck, other_in_deck,
                                 powders_on_bottom, other_on_bottom, mull_count)

    print(advice_string(best_action, mull_count))

    if best_action == 'regular':
        mull_count += 1
        powders_in_deck += powders_on_bottom
        other_in_deck += other_on_bottom
        powders_on_bottom = other_on_bottom = 0
    else:
        powders_to_bottom, other_to_bottom = best_action
        powders_on_bottom += powders_to_bottom
        other_on_bottom += other_to_bottom
        powders_in_deck -= powders_in_hand
        other_in_deck -= other_in_hand
