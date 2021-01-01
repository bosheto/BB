from binance.client import Client
from binance.enums import KLINE_INTERVAL_1MINUTE
from utils import get_proper_path
import os 
import sys
from keys import Pkey, Skey
from pandas import DataFrame as df
from pandas import read_csv as rcsv
from pandas.errors import *
from datetime import datetime


class DataRetriever:
    def __init__(self):
        self.client = Client(Pkey, Skey)

    def get_candle_data(self, _symbol, _interval, _start_time, _end_time='now', _limit=500, _folder_path=['CSV'], _mode='a'):
        try:
                #client = Client(Pkey, Skey)

                candles = self.client.get_historical_klines(symbol=_symbol, interval=_interval, start_str=_start_time, end_str=_end_time, limit=_limit)
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
                #final_data_frame['Ma-'+str(mas)] = final_data_frame['Close'].rolling(window=mas).mean()
                #final_data_frame['Ma-'+str(mal)] = final_data_frame['Close'].rolling(window=mal).mean()
                
                _folder_path.append(_symbol+'.csv')

                path = get_proper_path(_folder_path)
                
                final_data_frame.to_csv(path_or_buf=path, header=False, mode=_mode)
                return final_data_frame
        except KeyError:
            print('Pandas Key error retrying..')
            self.get_candle_data(_symbol=_symbol, _interval=_interval, _start_time=_start_time, _end_time=_end_time, _limit=_limit, _folder_path=_folder_path, _mode=_mode)


    def load_csv_data(self, _symbol, _file_path=[]):
        _file_path.append(_symbol + '.csv')
    
        data = rcsv(get_proper_path(_file_path), header=None)
        data.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote asset volume', 
                        'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume']
        data.set_index('Date', inplace=True)
    
        
        # data['Ma-'+str(mas)] = data['Close'].rolling(window=mas).mean()
        # data['Ma-'+str(mal)] = data['Close'].rolling(window=mal).mean()

        return data


    def get_current_price(self, _symbol):
        
        return float(self.client.get_avg_price(symbol=_symbol)['price'])



