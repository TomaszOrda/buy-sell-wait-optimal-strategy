from itertools import combinations
from math import prod


def _all_nonempty_combinations(array):
    result = []
    for number_of_elements in range(1, len(array)+1):
        for combination in combinations(range(len(array)), number_of_elements):
            result.append(list(combination))
    return result


def _alternate_prod_div(array, indexes):
    filtered_array = [array[i] for i in indexes]
    return prod(filtered_array[::2])/prod(filtered_array[1::2])


def strategy_optimizer_brute_aux(rates, margin=0.05,
                                 currency_1="CURR1", currency_2="CURR2"):
    currency_other = {
        currency_1: currency_2,
        currency_2: currency_1
    }

    optimal_strategy = {
            currency_1: {
                currency_1: ([], 1),
                currency_2: ([], 0)
            },

            currency_2: {
                currency_1: ([], 0),
                currency_2: ([], 1)
            }
    }
    currencies = [currency_1, currency_2]

    for strategy in _all_nonempty_combinations(rates):
        strategy_parity = len(strategy) % 2

        for curr1 in currencies:
            curr2 = curr1 if strategy_parity == 0 else currency_other[curr1]

            strategy_rate = _alternate_prod_div(rates, strategy)
            if curr1 == currency_1:
                strategy_rate = 1/strategy_rate
            strategy_rate *= (1-margin)**len(strategy)

            if optimal_strategy[curr1][curr2][1] < strategy_rate:
                optimal_strategy[curr1][curr2] = (strategy, strategy_rate)
    return optimal_strategy


def strategy_optimizer_brute(rates, margin=0.05,
                             currency_1="CURR1", currency_2="CURR2",
                             opening_currency="CURR1", closing_currency="CURR2"):

    if margin < 0:
        raise ValueError("Negative margin")

    if currency_1 == currency_2:
        raise ValueError("Indistinguishable currencies")

    if opening_currency not in [currency_1, currency_2]:
        raise ValueError("Unknown currency")
    if closing_currency not in [currency_1, currency_2]:
        raise ValueError("Unknown currency")

    if len(rates) == 0 and opening_currency != closing_currency:
        raise ValueError("Insufficient conversion rates")

    return strategy_optimizer_brute_aux(rates, margin, currency_1, currency_2)[opening_currency][closing_currency][0]
