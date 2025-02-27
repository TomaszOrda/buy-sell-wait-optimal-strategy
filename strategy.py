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


def brute_buy_sell_wait(rates, margin=0.05,
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


def strategy_optimizer(rates, margin=0.05,
                       currency_1="CURR1", currency_2="CURR2",
                       opening_currency=None, closing_currency=None):

    currencies = [currency_1, currency_2]

    def _dnc_buy_sell_wait(rates):
        if len(rates) <= 4:
            return brute_buy_sell_wait(rates, margin, currency_1, currency_2)
        middle = len(rates)//2
        left = _dnc_buy_sell_wait(rates[:middle])
        right = _dnc_buy_sell_wait(rates[middle:])
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

        for curr1 in currencies:
            for middle_currency in currencies:
                for curr2 in currencies:
                    combined_strategy_rate = left[curr1][middle_currency][1]*right[middle_currency][curr2][1]
                    if optimal_strategy[curr1][curr2][1] < combined_strategy_rate:
                        new_optimal_strategy = left[curr1][middle_currency][0] + \
                            [x + middle for x in right[middle_currency][curr2][0]]
                        optimal_strategy[curr1][curr2] = (new_optimal_strategy, combined_strategy_rate)
        return optimal_strategy

    optimal_strategy = _dnc_buy_sell_wait(rates)

    if closing_currency:
        for curr in currencies:
            optimal_strategy[curr] = optimal_strategy[curr][closing_currency]
    if opening_currency:
        optimal_strategy = optimal_strategy[opening_currency]

    return optimal_strategy
