from itertools import combinations
from math import prod

def strategyScanning(rates, margin=0.05, currency_1 = "CURR1", currency_2 = "CURR2", opening_currency = None, closing_currency = None):
  optimalStrategy = []
  
  potentialBuyingDay = None
  potentialBuySell = None
  
  if opening_currency == currency_2 and closing_currency = currency_1:
    rates = 1/rates

  def buySellIncome(buyRate, sellRate):
    return 1/buyRate * sellRate * (1-margin) * (1-margin)
    
  
  for day in range(len(rates)):
    if not potentialBuyingDay or rates[day]<lastBuyingDay: # new possible buying day
      potentialBuyingDay = day
      
    potentialBuySell = buySellIncome(rates[day], rates[potentialBuyingDay])
    if potentialBuySell>max(rates[day] - optimalStrategy[-1], 0): # we can have new buysell pair that is better than postponing buying and positive
      strategy + [potentialBuyingDay, day]
      elif rates[day] - optimalStrategy[-1] > 0: # we can postpone buying
         optimalStrategy[-1] = day
        
    return optmalStrategy
