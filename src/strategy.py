from itertools import combinations
from math import prod

def strategy(rates, margin=0.05, currency_1 = "CURR1", currency_2 = "CURR2"):
  currency_other = {
    currency_1:currency_2,
    currency_2:currency_1
  }
  currencies = [currency_1, currency_2]

  def all_nonempty_combinations(array):
    result = []
    for number_of_elements in range(1,len(array)+1):
      for combination in combinations(range(len(array)), number_of_elements):
        result.append(list(combination))
    return result

  def alternate_prod_div(array, indexes):
    filtered_array = [array[i] for i in indexes]
    return prod(filtered_array[::2])/prod(filtered_array[1::2])
  
  def brute_buy_sell_wait(rates):
    optimal_strategy = {
        currency_1: {
          currency_1: ([],1),
          currency_2: ([],0)
        },
  
        currency_2: {
          currency_1: ([],0),
          currency_2: ([],1)
        }
    }
  
    for strategy in all_nonempty_combinations(rates):
      strategy_parity = len(strategy)%2
  
      for curr1 in currencies:
          curr2 = curr1 if strategy_parity == 0 else currency_other[curr1]
  
          strategy_rate = alternate_prod_div(rates, strategy)
          if curr1 == currency_1: strategy_rate = 1/strategy_rate
          strategy_rate *= (1-margin)**len(strategy)
  
          if optimal_strategy[curr1][curr2][1]<strategy_rate:
            optimal_strategy[curr1][curr2] = (strategy, strategy_rate)
    return optimal_strategy
  
  def dnc_buy_sell_wait(rates):
    if len(rates)<=4:
      return brute_buy_sell_wait(rates)
    middle = len(rates)//2
    left  = dnc_buy_sell_wait(rates[:middle])
    right = dnc_buy_sell_wait(rates[middle:])
    optimal_strategy = {
        currency_1: {
          currency_1: ([],1),
          currency_2: ([],0)
        },
  
        currency_2: {
          currency_1: ([],0),
          currency_2: ([],1)
        }
    }
  
    for curr1 in currencies:
      for middle_currency in currencies:
        for curr2 in currencies:
          combined_strategy_rate = left[curr1][middle_currency][1]*right[middle_currency][curr2][1]
          if optimal_strategy[curr1][curr2][1]<combined_strategy_rate:
            new_optimal_strategy = left[curr1][middle_currency][0] + [x + middle for x in right[middle_currency][curr2][0]]
            optimal_strategy[curr1][curr2] = (new_optimal_strategy, combined_strategy_rate)
    return optimal_strategy



  
  return dnc_buy_sell_wait(rates)
