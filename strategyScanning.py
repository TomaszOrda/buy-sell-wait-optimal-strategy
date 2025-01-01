def strategyScanning(rates, margin=0.05, currency_1 = "CURR1", currency_2 = "CURR2", opening_currency = None, closing_currency = None):
  if not opening_currency: opening_currency = currency_1
  if not closing_currency: closing_currency = currency_2
    
  optimalStrategy = []
  
  potentialBuyingDay = 0
  
  if opening_currency == currency_2:
    rates = [1/r for r in rates]

  def buySellIncome(buyRate, sellRate):
    return 1/buyRate * sellRate * (1-margin) * (1-margin)
    
  
  for day in range(len(rates)):
    if rates[day]<rates[potentialBuyingDay]: # A better buying day found for some future buy-sell pair, as such there is no need for remmebering the previously considered buying day
      potentialBuyingDay = day
    
    potentialBuySellIncome = buySellIncome(rates[potentialBuyingDay], rates[day])
    
    if len(optimalStrategy) == 0:
      if potentialBuySellIncome > 1:
        optimalStrategy.extend([potentialBuyingDay, day])
        potentialBuyingDay = day
      continue
    
    if potentialBuySellIncome>max(rates[day]/rates[optimalStrategy[-1]], 1): # We can have new buysell pair that is better than postponing buying and positive
      optimalStrategy.extend([potentialBuyingDay, day])
      potentialBuyingDay = day
    elif rates[day] - rates[optimalStrategy[-1]] > 0: # We can postpone selling
       optimalStrategy[-1] = day
       potentialBuyingDay = day

  if opening_currency != closing_currency: # We will need additional buy or one less sell
    if len(optimalStrategy)==0:
        return [potentialBuyingDay]
    betterBuyingDay = potentialBuyingDay if rates[potentialBuyingDay] < rates[optimalStrategy[-2]] else optimalStrategy[-2]
    if potentialBuyingDay != optimalStrategy[-1] and buySellIncome(rates[optimalStrategy[-2]], rates[optimalStrategy[-1]]) * 1/rates[potentialBuyingDay] * (1-margin) > 1/rates[betterBuyingDay] * (1-margin): # Check if we get more from additional potential buying or from dropping last selling day (for the favor of potential or last buying day?)
      optimalStrategy.append(potentialBuyingDay)
    else:
      del optimalStrategy[-2:]
      optimalStrategy.append(betterBuyingDay)

  return optimalStrategy
