# -*- coding: utf-8 -*-
# **Installation**
"""

# **INSTALL QUANDL**
!pip install quandl
!pip install yfinance
import quandl
!pip install --upgrade pandas-datareader

"""# **Stock Analysis**"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib import style
# %matplotlib inline
import seaborn as sns
import quandl
import yfinance as yf
from matplotlib.widgets import Slider
from pandas.plotting import scatter_matrix

from datetime import datetime

quandl.ApiConfig.api_key = '7rnqBK1qvrthvZWqJbnp'

stock_list = ['MSFT','AMZN','GOOG']

df1 = quandl.get_table('WIKI/PRICES', ticker = stock_list, paginate = True)
df1

#last 1 year
start = datetime(2017,1,1)
end = datetime(2018,1,1)

file1 = quandl.get_table('WIKI/PRICES', ticker = stock_list, date = {'gte':start,'lte':end}, paginate=True).set_index("date")
stocks = yf.download(['MSFT','AMZN','GOOG'], start= '2017-01-01', end= '2018-01-01')
file1

#closing price
q1 = df1[df1.ticker == 'AMZN']
q1
q2 = df1[df1.ticker == 'GOOG']
q2
q3 = df1[df1.ticker == 'MSFT']
q3

plt.rcParams['figure.figsize']=(15.0,8.0)
style.use('ggplot')
plt.subplots_adjust(hspace= 0.25)
plt.subplot(2,2,1)
plt.title('Amazon Closing Price Analysis')
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.plot(q1.date,q1.close,color= 'b')
plt.legend(q1.ticker)
plt.subplot(2,2,2)
plt.title('Google Closing Price Analysis')
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.plot(q2.date,q2.close,color= 'g')
plt.legend(q2.ticker)
plt.subplot(2,2,3)
plt.title('Microsoft Closing Price Analysis')
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.plot(q3.date,q3.close,color= 'c')
plt.legend(q3.ticker)
plt.show()

plt.rcParams['figure.figsize']=(15.0,8.0) 
style.use('ggplot')
plt.subplots_adjust(top=9,bottom=.123)
plt.subplot(4,1,2)
plt.title('Amazon Stock Volume Analysis')
q1['volume'].plot(legend=True,color='b')
plt.subplot(4,1,3)
plt.title('Google Stock Volume Analysis')
q2['volume'].plot(legend=True,color='g')
plt.subplot(4,1,4)
plt.title('Microsoft Stock Volume Analysis')
q3['volume'].plot(legend=True,color='c')
plt.show()

plt.rcParams['figure.figsize']=(25.0,15.0)
style.use('ggplot')
plt.subplots_adjust(hspace =0.25)
plt.subplot(2,2,1)
plt.title ('Closing Price Analysis')
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.plot(q1.date,q1.close,color='b')
plt.plot(q2.date,q2.close,color='g')
plt.plot(q3.date,q3.close,color='c')
plt.legend(df1.ticker.unique())
plt.show()

#plotting percentage change for Amazon's stock
df1['percentage_change']=df1['close'].pct_change()*100
df1

dt = df1[df1.percentage_change > 1.0]
dt

#percentage change for AMAZON's stock
pc = dt[dt['ticker']=='AMZN']

plt.rcParams['figure.figsize']=(20.0,8.0)
style.use('ggplot')
plt.title('Amazon\'s Percentage Change')
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.plot(pc.date,pc.percentage_change,color='g')
plt.show()

#plotting daily return change
df1['daily_return'] = df1['adj_close'].pct_change()
df1

#Plotting amazon's daily return change
plt.title ('Amazon\'s daily return change')
df1['daily_return'].plot(figsize=(20,8),legend=True,linestyle='-',marker='H')

sns.factorplot(x_='q1',y_='q2',data=file1,height=5,aspect=3)

ama=web.DataReader("AMZN",'yahoo',start,end)
goog=web.DataReader("GOOGL",'yahoo',start,end)
micro=web.DataReader("MSFT",'yahoo',start,end)
stocks1 = pd.concat ( [ama['Open'], goog['Open'], micro['Open']] , axis = 1)
stocks1.columns = [ 'Amazon Open', 'Google Open', 'Microsoft Open' ]

scatter_matrix(stocks1, figsize=(8, 8) )

stocksData = stocks.loc[:,"Close"].copy()
data = stocksData.pct_change().dropna()
data = data.describe().T.loc[:,["mean", "std"]]
data["mean"] = data["mean"] * 251
data["std"] = data["std"] * np.sqrt(251)
data.plot.scatter(figsize= (20,10), fontsize=20, x="std", y="mean")
for idx in data.index:
     plt.annotate(idx,xy=(data.loc[idx,"std"]+0.005,data.loc[idx,"mean"]+0.005),xytext=(40,40), textcoords='offset points',ha='center',va='bottom',arrowprops=dict(arrowstyle='-',connectionstyle='arc3,rad=0.3'))
