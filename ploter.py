import plotly.offline as py
import plotly.graph_objs as go
from datetime import datetime
from dataB import get_binance_candle_data
from binance.client import Client
from indicators import MovingAverage

data = get_binance_candle_data('LINKUSDT', Client.KLINE_INTERVAL_30MINUTE)

rolling_mean = MovingAverage(data, 7, 'green')
rolling_mean_long = MovingAverage(data, 25, 'orange')

trace = go.Ohlc(
    x = data.index[:],
    open = data['Open'],
    high = data['High'],
    low = data['Low'],
    close = data['Close'],
    name = 'LINK USDT',
    increasing=dict(line=dict(color='blue')),
    decreasing=dict(line=dict(color='red')),
)

MA = go.Scatter(x=data.index[:], y=rolling_mean['data'], name='MA ({})'.format(rolling_mean['scale']), line=dict(color=rolling_mean['color']))
MA1 = go.Scatter(x=data.index[:], y=rolling_mean_long['data'], name='MA ({})'.format(rolling_mean_long['scale']), line=dict(color=rolling_mean_long['color']))

plot_data = [trace, MA, MA1]
layout = {
    'title':'LINK USDT',
    'yaxis':{'title':'Price per coin'}
}

fig = dict(data=plot_data, layout=layout)

py.plot(fig, filename='Charts\\crypto.html')