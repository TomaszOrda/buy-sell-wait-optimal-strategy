from strategy_brute import strategy_optimizer_brute_aux


def strategy_optimizer(rates, margin=0.05,
                       currency_1="CURR1", currency_2="CURR2",
                       opening_currency=None, closing_currency=None):

    if opening_currency not in [currency_1, currency_2, None]:
        raise ValueError("Unknown currency")
    if closing_currency not in [currency_1, currency_2, None]:
        raise ValueError("Unknown currency")

    currencies = [currency_1, currency_2]

    def _dnc_buy_sell_wait(rates):
        if len(rates) <= 4:
            return strategy_optimizer_brute_aux(rates, margin, currency_1, currency_2)
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
