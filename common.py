def _validate_arguments(rates, margin, currency_1, currency_2, opening_currency, closing_currency):
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
