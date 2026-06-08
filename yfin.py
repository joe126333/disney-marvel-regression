import yfinance as yf
dat = yf.Ticker('DIS')
date_list = []

prices = dat.history(interval = '1d', start = '2008-01-01', end = '2026-06-01')
prices.to_csv('daily_disney_stock.csv')

new_prices = prices.drop(columns = ['Dividends', 'Stock Splits'])
new_prices.to_csv('daily_disney_stock_reduced.csv')
