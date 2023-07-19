import random

def create_portfolio(stocks):
    print(f"stocks: {stocks}")
    dict = {}
    num = 1
    if len(stocks) < 1:
        return dict
    for i in range(0, len(stocks) - 1):
        # generate a number number between 0 and num (decimal)
        stock_weight = random.random() * num
        dict[stocks[i]] = stock_weight
        num -= stock_weight
    dict[stocks[len(stocks) - 1]] = num
    return dict

# how can i pick a random decimal number between 0 and 1
#a: random.random()

    
