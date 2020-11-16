import plotly.offline as py
import plotly.graph_objs as go
from datetime import datetime
from dataB import load_binance_data_from_csv
from binance.client import Client
from indicators import MA, EMA
from strategy import find_entry_point
from file_manager import update_curency_file

data = load_binance_data_from_csv('LINKUSDT')


rolling_mean = MA(data, 7, 'purple')
rolling_mean_long = MA(data, 25, 'orange')
exponential_MA = EMA(data, 7, 'cyan')
exponetial_MA_long = EMA(data, 25, 'orange')

#find_entry_point(data, rolling_mean['data'], rolling_mean_long['data'])

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


plot_data = [candle, MA_chart, MA1_chart] #, exMA, exMA_long]
layout = {
    'title':'LINK USDT',
    'yaxis':{'title':'Price per coin'}
}

fig = dict(data=plot_data, layout=layout)

#py.plot(fig, filename='Charts\\crypto.html')

def create_debug_chart(data, indicators, entry_positions, sell_positions):

    mean = indicators[0]
    mean_long = indicators[1]

    candle = go.Candlestick(
    x = data.index[:],
    open = data['Open'],
    high = data['High'],
    low = data['Low'],
    close = data['Close'],
    name = 'BNB USDT',
    )

    sma_trace = go.Scatter(x=data.index[:], y =mean['data'], name='Ma ({})'.format(mean['scale']), line=dict(color=mean['color']))
    lma_trace = go.Scatter(x=data.index[:], y =mean_long['data'], name='Ma ({})'.format(mean_long['scale']), line=dict(color=mean_long['color']))
    
    entry_pos = go.Scatter(
        x=data.index[:],
        y = entry_positions,
        mode='markers',
        line=dict(color='green'),
        name='Entry points'

    )

    sell_point = go.Scatter(
        x = data.index[:],
        y = sell_positions,
        mode='markers',
        line=dict(color='red'),
        name='Sell points'

    )
    plot_data = [candle, sma_trace, lma_trace, entry_pos, sell_point]
    
    layout = {
        'title' : 'BNB-USDT Debug',
        'yaxis' : {'title' : 'Price per coin'}
    }

    fig = dict(data=plot_data, layout=layout)
    py.plot(fig, filename='Charts\\Debug.html')