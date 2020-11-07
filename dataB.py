from binance.client import Client
from datetime import datetime
from pandas import DataFrame as df 
import keys


def get_binance_candle_data(symbol, interval):
    client = Client(keys.Pkey, keys.Skey)

    candles = client.get_klines(symbol=symbol, interval=interval  )

    candles_data_frame = df(candles)

    candles_data_frame_date = candles_data_frame[0]

    final_date = []

    for time in candles_data_frame_date.unique():
        readable = datetime.fromtimestamp(int(time/1000))
        final_date.append(readable)

    candles_data_frame.pop(0)
    candles_data_frame.pop(11)
    candles_data_frame.columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote asset volume', 
    'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume']
    dataframe_final_date = df(final_date)
    dataframe_final_date.columns = ['Date']
    final_data_frame = candles_data_frame.join(dataframe_final_date)

    final_data_frame.set_index('Date', inplace=True)
    return final_data_frame

print(get_binance_candle_data(symbol='LINKUSDT', interval=Client.KLINE_INTERVAL_1HOUR))