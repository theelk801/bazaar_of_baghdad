from prob_functions import *


def get_input(prompt):
    while True:
        try:
            return int(input(prompt + '\n'))
        except (ValueError, NameError):
            print('Please enter a number')


powders_in_hand = get_input('How many Serum Powder are in your hand?')
other_in_hand = get_input('How many other cards are in your hand?')
powders_on_bottom = get_input(
    'How many Serum Powder are on the bottom of your library?')
other_on_bottom = get_input(
    'How many other cards are on the bottom of your library?')
powders_in_deck = get_input(
    'How many Serum Powder are in your deck (but that you know are not on the bottom)?'
)
other_in_deck = get_input(
    'How many other cards are in your deck (but that you know are not on the bottom)?'
)
mull_count = get_input(
    'How many times have you taken a normal mulligan (i.e. how many cards will you need to put on the bottom)?'
)

action_to_take(powders_in_hand, other_in_hand, powders_in_deck, other_in_deck,
               powders_on_bottom, other_on_bottom, mull_count)
