import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import yfinance as yf
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


# @param: portfolio: a list of portfolio ticker symbols
def covariance_matrix(portfolio):
    for ticker in portfolio:
        average_daily_return = snp_df['Daily Return'].mean()

# @param share_vector: a vector of shares
# @param covariance_matrix: a covariance matrix of the shares
def variance(share_vector, covariance_matrix):
    return np.dot((share_vector.T @ covariance_matrix).T, share_vector)