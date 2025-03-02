from common import _validate_arguments


def _buy_sell_income(buy_rate, sell_rate, margin):
    return 1/buy_rate * sell_rate * (1-margin) * (1-margin)


def strategy_optimizer_scanning(rates, margin=0.05,
                                currency_1="CURR1", currency_2="CURR2",
                                opening_currency="CURR1", closing_currency="CURR2"):

    _validate_arguments(rates, margin, currency_1, currency_2, opening_currency, closing_currency)

    optimal_strategy = []

    potential_buying_day = 0

    if opening_currency == currency_2:
        rates = [1/r for r in rates]

    for day, rate in enumerate(rates):
        if rate < rates[potential_buying_day]:
            # A better buying day found for some future buy-sell pair,
            # as such there is no need for remmebering the previously considered buying day
            potential_buying_day = day
            continue

        potential_buy_sell_income = _buy_sell_income(rates[potential_buying_day], rate, margin)

        if len(optimal_strategy) == 0:
            if potential_buy_sell_income > 1:
                optimal_strategy.extend([potential_buying_day, day])
                potential_buying_day = day
            continue

        if potential_buying_day != optimal_strategy[-1] and \
           potential_buy_sell_income > max(rate/rates[optimal_strategy[-1]], 1):
            # We can have new buysell pair that is better than postponing buying and positive
            optimal_strategy.extend([potential_buying_day, day])
            potential_buying_day = day
        elif rate - rates[optimal_strategy[-1]] > 0:
            # We can postpone selling
            optimal_strategy[-1] = day
            potential_buying_day = day

    if opening_currency != closing_currency:
        # We will need additional buy or one less sell
        if len(optimal_strategy) == 0:
            return [potential_buying_day]
        better_buying_day = \
            potential_buying_day \
            if rates[potential_buying_day] < rates[optimal_strategy[-2]] \
            else optimal_strategy[-2]

        # Check if we get more from
        # additional potential buying or
        # from dropping last selling day
        delta_of_adding_a_buy = \
            _buy_sell_income(rates[optimal_strategy[-2]],
                             rates[optimal_strategy[-1]],
                             margin) \
            * 1/rates[potential_buying_day] * (1-margin)

        delta_of_dropping_last_sell = 1/rates[better_buying_day] * (1-margin)

        if potential_buying_day != optimal_strategy[-1] and delta_of_adding_a_buy > delta_of_dropping_last_sell:
            optimal_strategy.append(potential_buying_day)
        else:
            del optimal_strategy[-2:]
            optimal_strategy.append(better_buying_day)

    return optimal_strategy
