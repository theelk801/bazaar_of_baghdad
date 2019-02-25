With the new London mulligan rule, much has been discussed regarding its effect on combo decks. While the probabilities of various situations can be relatively straightforward, the scenario of utilizing aggressive mulligans to have a turn one [Bazaar of Baghdad](https://scryfall.com/card/vma/294/bazaar-of-baghdad) in vintage dredge is complicated by the usage of [Serum Powder](https://scryfall.com/card/ima/228/serum-powder) to increase likelihoods.

## Outline of the London mulligan rule
The new London mulligan rule works as follows:
1) If you choose to mulligan and you have at least one card in hand, shuffle your hand into your library and draw seven new cards
2) Put n cards from your hand on the bottom of your library, where n is the amount of times you have chosen to mulligan
3) Repeat if necessary

## Serum Powder
The addition of Serum Powder allows a player to instead exile their hand and draw that many cards whenever they could otherwise mulligan, and so we can have several options at any given point. More importantly, the cards we choose to put on the bottom before we use Serum Powder can potentially make a difference as well.

## Explanation of methods
The approach is therefore as follows: To determine the probability of a hand having or mulliganing into a Bazaar, we look at the probability of each possible choice being a success and choose that outcome. However, each choice includes more choices, and so we create a recursive function which weighs each choice and returns the best.

## Description of code
The function `prob_of_good_hand` computes the overall probability of having a Bazaar in one's opening hand given correct mulligan decisions, and the function `action_to_take` provides the appropriate action to take given information about what is in the player's hand. Additionally, there is a script `decider.py` which provides a questionnaire for mulligan decisions.

## Results
Using the code, we see that a player has a roughly 99.05% chance of having a Bazaar of Baghdad in their opening hand.

## Collaboration
If you find any errors or have any questions, please do not hesitate to contact me or open an issue or pull request.
