import plotly.offline as py
import plotly.graph_objs as go
from datetime import datetime
from dataB import get_binance_candle_data
from binance.client import Client
from indicators import MA, EMA

data = get_binance_candle_data('LINKUSDT', Client.KLINE_INTERVAL_15MINUTE, '2 day ago UTC')

rolling_mean = MA(data, 7, 'purple')
rolling_mean_long = MA(data, 25, 'orange')
exponential_MA = EMA(data, 7, 'cyan')
exponetial_MA_long = EMA(data, 25, 'orange')

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

candle = go.Candlestick(
    x = data.index[:],
    open = data['Open'],
    high = data['High'],
    low = data['Low'],
    close = data['Close'],
    name = 'LINK USDT',
    
    )

MA_chart = go.Scatter(x=data.index[:], y=rolling_mean['data'], name='MA ({})'.format(rolling_mean['scale']), line=dict(color=rolling_mean['color']))
MA1_chart = go.Scatter(x=data.index[:], y=rolling_mean_long['data'], name='MA ({})'.format(rolling_mean_long['scale']), line=dict(color=rolling_mean_long['color']))
exMA = go.Scatter(x=data.index[:], y=exponential_MA['data'], name= 'EMA ({})'.format(exponential_MA['scale'], line=dict(color=exponential_MA['color'])))
exMA_long = go.Scatter(x=data.index[:], y=exponetial_MA_long['data'], name= 'EMA ({})'.format(exponetial_MA_long['scale'], line=dict(color=exponetial_MA_long['color'])))


plot_data = [candle, MA_chart, MA1_chart, exMA, exMA_long]
layout = {
    'title':'LINK USDT',
    'yaxis':{'title':'Price per coin'}
}

fig = dict(data=plot_data, layout=layout)

py.plot(fig, filename='Charts\\crypto.html')