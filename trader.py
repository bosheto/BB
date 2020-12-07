from binance.client import Client
from binance.enums import *
from keys import Pkey, Skey
from time import time
from datetime import datetime
from pandas import DataFrame as df 
import pandas as pd

class Trader:

    def __init__(self):
        # General stuff
        self.data = None
        self.hasAssets = False
        self.symbol = 'LINKUSDT'
        self.short_ma = None
        self.long_ma = None

        # Trade info
        self.buy_price = 0
        self.sell_price = 0

        # Stop loss 
        self.stop_loss_price = 0
        self.stop_loss_amount = 0.01
        self.stop_loss_update_amount = 0.012

        # Timer stuff
        self.slow_update = 60
        self.fast_update = 15
        self.buy_last_update = time()
        self.sell_last_update = time()
        self.update_time_short = 0
        self.update_time_long = 0

    def update(self):
        self.find_exit_point()
        self.find_entry_point()
        

    def find_entry_point(self ):
        if time() - self.buy_last_update >= self.slow_update - self.update_time_long:
            tt = time()
            self.get_candle_data()
            self.data = self.load_binance_data_from_csv()
            self.short_ma = self.data['Close'].rolling(window=7).mean()
            self.long_ma = self.data['Close'].rolling(window=25).mean()
           
            # Buy Coins
            if not self.hasAssets and self.short_ma[-1] > self.long_ma[-1] and self.short_ma[-1] > self.short_ma[-2]:
                self.hasAssets = True
                self.buy_price = self.get_price_data()
                self.stop_loss_price = self.buy_price - self.stop_loss_amount
                print('Buy order at {}'.format(self.buy_price))
                
            
            print(self.get_timestamp() + 'Buy Update')
            self.buy_last_update = time()
            self.update_time_long = time() - tt
    
    def find_exit_point(self):
        if self.hasAssets and time() - self.sell_last_update >= self.fast_update - self.update_time_short:
            tt = time()
            current_price = self.get_price_data()

            # Sell Coins 
            if current_price < self.stop_loss_price or self.short_ma[-1] < self.short_ma[-2]:
                self.hasAssets = False
                self.sell_price = current_price
                print(self.get_timestamp() +'Sold at {0} with a profit of {1} \a'.format(self.sell_price, self.truncate((self.sell_price - self.buy_price), 4)))
                self.buy_price = 0
                self.sell_price = 0
                self.stop_loss_price = 0

            # Update Stop loss
            if current_price >= self.buy_price + self.stop_loss_update_amount:
                self.stop_loss_price = current_price - self.stop_loss_amount
            print(self.get_timestamp() + ' Sell update')
            self.sell_last_update = time()
            self.update_time_short = time() - tt
    
    def get_timestamp(self):
        timestamp = '[{0}:{1}:{2}] '.format(str(datetime.now().hour),str(datetime.now().minute), str(datetime.now().second))
        return timestamp

    def get_candle_data(self):
        try:
            client = Client(Pkey, Skey)

            candles = client.get_historical_klines(symbol=self.symbol, interval=KLINE_INTERVAL_1MINUTE, start_str='1 minute ago UTC')
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
            path = 'CSV\\' + self.symbol + '.csv'
            final_data_frame.to_csv(path_or_buf=path, header=False, mode='a')
            return final_data_frame
    
        except KeyError:
            print('Pandas Key error retrying..')
            self.get_candle_data()

    def get_price_data(self):
        client = Client(Pkey, Skey)
        return float(self.truncate(client.get_avg_price(symbol=self.symbol)['price'], 4))

    
    def load_binance_data_from_csv(self):
        filename = 'CSV\\' + self.symbol + '.csv'
        with open(filename, 'r') as f:
            data = pd.read_csv(filename)
            data.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote asset volume', 
            'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume']
            data.set_index('Date', inplace=True)
            
            f.close()
            return data

    def truncate(self,f, n):
        '''Truncates/pads a float f to n decimal places without rounding'''
        s = '{}'.format(f)
        if 'e' in s or 'E' in s:
            return '{0:.{1}f}'.format(f, n)
        i, p, d = s.partition('.')
        return float('.'.join([i, (d+'0'*n)[:n]]))
