import pandas_datareader as pd 
import plotly.offline as py
import plotly.graph_objs as go
import datetime

start_date = datetime.datetime(2017,1,1)
end_date = datetime.datetime.now()

AAPL = pd.DataReader('AAPL', 'yahoo', start_date, end_date)

print(AAPL.tail(10))

trace = go.Ohlc(
    x = AAPL.index[:],
    open = AAPL['Open'],
    high = AAPL['High'],
    low = AAPL['Low'],
    close = AAPL['Close'],
    name = 'AAPL',
    increasing=dict(line=dict(color='blue')),
    decreasing=dict(line=dict(color='red')),
)

data = [trace]
layout = {
    'title' : 'AAPL STOCK',
    'yaxis' : {'title': 'Price per share'}
}

fig = dict(data=data,layout=layout)
py.plot(fig, filename='stonks.html')