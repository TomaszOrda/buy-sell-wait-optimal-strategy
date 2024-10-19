def strategyScanning(rates, margin=0.05, currency_1 = "CURR1", currency_2 = "CURR2", opening_currency = None, closing_currency = None):
  if not opening_currency: opening_currency = currency_1
  if not closing_currency: closing_currency = currency_2
    
  optimalStrategy = []
  
  potentialBuyingDay = None
  potentialBuySell = None
  
  if opening_currency == currency_2:# and closing_currency == currency_1:
    rates = 1/rates

  def buySellIncome(buyRate, sellRate):
    return 1/buyRate * sellRate * (1-margin) * (1-margin)
    
  
  for day in range(len(rates)):
    if not potentialBuyingDay or rates[day]<potentialBuyingDay: # new possible buying day
      potentialBuyingDay = day
      
    potentialBuySell = buySellIncome(rates[day], rates[potentialBuyingDay])
    if potentialBuySell>max(rates[day] - optimalStrategy[-1], 0): # we can have new buysell pair that is better than postponing buying and positive
      optimalStrategy.append([potentialBuyingDay, day])
    elif rates[day] - optimalStrategy[-1] > 0: # we can postpone selling
       optimalStrategy[-1] = day

  if opening_currency != closing_currency: #we will need additional buy or one less sell
    betterBuyingDay = #argmax optimalStrategy[-2], potentialBuyingDay
    if buySellIncome(rates[optimalStrategy[-2], rates[optimalStrategy[-1]) * 1/rates[potentialBuyingDay] * (1-margin) > 1/rates[betterBuyingDay] * (1-margin): #check if we get more from additional potential buying or from dropping last selling day (for the favor of potential or last buying day?)
      optimalStrategy.append([potentialBuyingDay])
      #add potential buying day to strategy
    else:
      optimalStrategy.remove(-1)
      optimalStrategy.remove(-1)
      optimalStrategy.append([betterBuyingDay])
      #remove last buy and sell, add better buying day 

  return optimalStrategy
