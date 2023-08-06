import random
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

snp_df = yf.download('SPY', period='5y')
nasdaq_df = yf.download('^IXIC', period='5y')

snp_df['Daily Return'] = (snp_df['Adj Close'] - snp_df['Open']) / snp_df['Open']
nasdaq_df['Daily Return'] = (nasdaq_df['Adj Close'] - nasdaq_df['Open']) / nasdaq_df['Open']

# @param stocks: a list of stocks
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

# @param portfolio: a dictionary with 
# * keys are stocks
# * values are a list of [weight in portfolio, expected return]
def expected_returns(portfolio):
    expected_return = 0
    for key, value in portfolio.items():
        expected_return += value[0] * value[1]
    return expected_return

# @param portfolio: a dictionary with
# * keys are stocks
# * values are a list of [weight in portfolio, beta]
def portfolio_beta(portfolio):
    beta = 0
    for key, value in portfolio.items():
        beta += value[0] * value[1]
    return beta

# @param stock: a string representing a stock
def beta(stock):
    # Perform a linear regression on the stock's daily returns with the dependent variable being stocks daily returns and the independent variable being the S&P 500's daily returns
    stock_df = yf.download(stock, period='5y')
    stock_df['Daily Return'] = (stock_df['Adj Close'] - stock_df['Open']) / stock_df['Open']
    stock_daily_returns = stock_df['Daily Return'].values.reshape(-1, 1)
    
    snp_daily_returns = snp_df['Daily Return'].values.reshape(-1, 1)
    
    model = LinearRegression().fit(snp_daily_returns, stock_daily_returns)
    beta = model.coef_[0][0]
    return beta

# 1. Value the securities in the portfolio

# @param stock: a string representing a stock
def expected_return(stock):
    # obtain a dataframe of the stock from yfinance
    stock_df = yf.download(stock, period='5y')

    average_daily_return = ((stock_df['Adj Close'] - stock_df['Open']) / stock_df['Open']).mean()
    
    average_weekly_return = stock_df['Adj Close'].pct_change(7).mean()
    average_monthly_return = stock_df['Adj Close'].pct_change(30).mean()
    average_yearly_return = stock_df['Adj Close'].pct_change(365).mean()

    print(f"average daily return: {average_daily_return}")
    print(f"average weekly return: {average_weekly_return}")
    print(f"average monthly return: {average_monthly_return}")
    print(f"average yearly return: {average_yearly_return}")

    # adjust for risk using CAPM 
    # CAPM = risk free rate + beta * (expected market return - risk free rate)
    expected_market_returns = 0.0381
    adjusted_return = expected_market_returns + beta(stock) * (average_daily_return - expected_market_returns)
    return adjusted_return

print(f"adjusted daily returns: {expected_return('AAPL')}")

# 2. Calculate the desired asset allocation

# @param stocks: a list of stocks
def correlation(stocks):
    # create a correlation matrix (2D array) of the stocks
    correlation_matrix = np.zeros((len(stocks), len(stocks)))
    for i in range(0, len(stocks)):
        for j in range(0, len(stocks)):
            correlation_matrix[i][j] = np.corrcoef(yf.download(stocks[i], period='5y')['Adj Close'], yf.download(stocks[j], period='5y')['Adj Close'])[0][1]
            correlation_matrix[j][i] = correlation_matrix[i][j]


def expected_return_range(low, high):
    return tuple(low, high)

def efficient_frontier():
    pass



# 3. Calculations to optimize the portfolio to gain highest return with lowest risk

# 4. Using financial analysis tools to analyze the portfolio and see if it 
# #   meets expections and making necessary changes when market conditions change
