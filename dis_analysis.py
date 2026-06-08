import pandas as pd
import numpy as np
import scipy as scipy
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


stocks = pd.read_csv('daily_disney_stock_reduced.csv')
movies = pd.read_csv('mcu_movies_table.csv')
movies = movies.set_index('Date', drop = False)

avg_price = []
test1 = []

# truncate stocks to match movie dates
stocks = stocks.drop(stocks.index[0:84])
stocks = stocks.drop(stocks.index[4400:])
stocks = stocks.set_index('Date')

# failed attempt to iterate to compute average stock prices
# for idx in range(0, len(movies) - 1):
#     test1.append(stocks['Close'].loc[movies['Date'].iloc[idx]:movies['Date'].iloc[idx + 1]].mean())

# compute average stock based on movies release dates
avg_price.append(stocks['Close'].loc['2008-05-02':'2008-06-13'].mean())
avg_price.append(stocks['Close'].loc['2008-06-13':'2010-05-07'].mean())
avg_price.append(stocks['Close'].loc['2010-05-07':'2011-05-06'].mean())
avg_price.append(stocks['Close'].loc['2011-05-06':'2011-07-22'].mean())
avg_price.append(stocks['Close'].loc['2011-07-22':'2012-05-04'].mean())
avg_price.append(stocks['Close'].loc['2012-05-04':'2013-05-03'].mean())
avg_price.append(stocks['Close'].loc['2013-05-03':'2013-11-08'].mean())
avg_price.append(stocks['Close'].loc['2013-11-08':'2014-04-04'].mean())
avg_price.append(stocks['Close'].loc['2014-04-04':'2014-08-01'].mean())
avg_price.append(stocks['Close'].loc['2014-08-01':'2015-05-01'].mean())
avg_price.append(stocks['Close'].loc['2015-05-01':'2015-07-17'].mean())
avg_price.append(stocks['Close'].loc['2015-07-17':'2016-05-06'].mean())
avg_price.append(stocks['Close'].loc['2016-05-06':'2016-11-04'].mean())
avg_price.append(stocks['Close'].loc['2016-11-04':'2017-05-05'].mean())
avg_price.append(stocks['Close'].loc['2017-05-05':'2017-07-07'].mean())
avg_price.append(stocks['Close'].loc['2017-07-07':'2017-11-03'].mean())
avg_price.append(stocks['Close'].loc['2017-11-03':'2018-02-16'].mean())
avg_price.append(stocks['Close'].loc['2018-02-16':'2018-04-27'].mean())
avg_price.append(stocks['Close'].loc['2018-04-27':'2018-07-06'].mean())
avg_price.append(stocks['Close'].loc['2018-07-06':'2019-03-08'].mean())
avg_price.append(stocks['Close'].loc['2019-03-08':'2019-04-26'].mean())
avg_price.append(stocks['Close'].loc['2019-04-26':'2019-07-02'].mean())
avg_price.append(stocks['Close'].loc['2019-07-02':'2021-07-09'].mean())
avg_price.append(stocks['Close'].loc['2021-07-09':'2021-09-03'].mean())
avg_price.append(stocks['Close'].loc['2021-09-03':'2021-11-05'].mean())
avg_price.append(stocks['Close'].loc['2021-11-05':'2021-12-17'].mean())
avg_price.append(stocks['Close'].loc['2021-12-17':'2022-05-06'].mean())
avg_price.append(stocks['Close'].loc['2022-05-06':'2022-07-08'].mean())
avg_price.append(stocks['Close'].loc['2022-07-08':'2022-11-11'].mean())
avg_price.append(stocks['Close'].loc['2022-11-11':'2023-02-17'].mean())
avg_price.append(stocks['Close'].loc['2023-02-17':'2023-05-05'].mean())
avg_price.append(stocks['Close'].loc['2023-05-05':'2023-11-10'].mean())
avg_price.append(stocks['Close'].loc['2023-11-10':'2024-07-26'].mean())
avg_price.append(stocks['Close'].loc['2024-07-26':'2025-02-14'].mean())
avg_price.append(stocks['Close'].loc['2025-02-14':'2025-05-02'].mean())
avg_price.append(stocks['Close'].loc['2025-05-02':'2025-07-25'].mean())
avg_price.append(stocks['Close'].loc['2025-07-25':'2025-10-27'].mean())

# compute series for profit
movies['Profit'] = movies['Total'] - movies['Budget']
movie_profit = movies['Profit'].tolist()

# make dataframe from lists
profit_stock = pd.DataFrame({'Profit': movie_profit, 'Stock': avg_price})

# compute correlation
pear_r = scipy.stats.pearsonr(profit_stock['Profit'], profit_stock['Stock'])
print(pear_r)

# linear regression
X = profit_stock['Profit'].values
X = X.reshape(len(X), 1)
Y = profit_stock['Stock'].values
Y = Y.reshape(len(Y), 1)

model = LinearRegression()
model.fit(X, Y)
pred = model.predict(X)

plt.figure(figsize = (8,6))
plt.scatter(X, Y, color = 'blue')
plt.plot(X, pred, color = 'red', linewidth = 2, label = 'Regression Line')
plt.title('Linear Regression for Profit and Average Stock Price')
plt.xlabel('Profit')
plt.ylabel('Avg Stock Price')
plt.legend()
plt.grid(True)
plt.show()
plt.savefig('lin_reg.png')

# polynomial regression
poly = PolynomialFeatures(degree = 2)
X_poly = poly.fit_transform(X)
poly.fit(X_poly, Y)
poly_reg = LinearRegression()
poly_reg.fit(X_poly, Y)

plt.scatter(X, Y, color = 'blue')
plt.plot(X, poly_reg.predict(poly.fit_transform(X)), color = 'red')
plt.title('Polynomial Regression for Profit and Average Stock Price')
plt.xlabel('Profit')
plt.xlabel('Avg Stock Price')
plt.show()
plt.savefig('quad_reg.png')
