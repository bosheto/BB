from binance.client import Client
from datetime import datetime
from pandas import DataFrame as df 
import pandas as pd
import keys

'''Get candle data from binance
    Params
    symbol : the coin pair 
    interval : data interval
    from_time : start time 
'''
def get_binance_candle_data(symbol, interval, from_time):
    try:
        client = Client(keys.Pkey, keys.Skey)

        candles = client.get_historical_klines(symbol=symbol, interval=interval, start_str=from_time )
        #candles = client.get_klines(symbol=symbol, interval=interval  )


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
        #final_data_frame['MA-7'] = final_data_frame['Close'].rolling(window=7).mean()
        
        path = 'CSV\\' + symbol + '.csv'
        final_data_frame.to_csv(path_or_buf=path, header=False, mode='w')
        return final_data_frame
    
    except KeyError:
        print('Pandas Key error retrying..')
        get_binance_candle_data(symbol, interval, from_time)

def load_binance_data_from_csv(symbol):
    filename = 'CSV\\' + symbol + '.csv'
    with open(filename, 'r') as f:
        data = pd.read_csv(filename)
        data.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote asset volume', 
        'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume']
        data.set_index('Date', inplace=True)
        
        f.close()
        return data

def check_for_missing_data(symbol):
    pass

def get_current_price(symbol):
    client = Client(keys.Pkey, keys.Skey)
    raw_price = client.get_avg_price(symbol)['price']
    return float(raw_price)
