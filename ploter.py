import plotly.offline as py
import plotly.graph_objs as go

from dataB import get_binance_candle_data
from binance.client import Client

data = get_binance_candle_data('LINKUSDT', Client.KLINE_INTERVAL_30MINUTE)

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

plot_data = [trace]
layout = {
    'title':'LINK USDT',
    'yaxis':{'title':'Price per coin'}
}

fig = dict(data=plot_data, layout=layout)

py.plot(fig, filename='crypto.html')