
from binance.client import Client
from binance.enums import *
from keys import Pkey, Skey
from time import time
from datetime import datetime
from pandas import DataFrame as df 
from enum import Enum
import pandas as pd
import os
import random as rand
import sys

class Trader:

    def __init__(self, mode=0):
        # General stuff
        self.name = 'Trader'
        self.version = 'a1.0'
        self.mode = self.validate_selected_mode(mode)
        self.data = None
        self.hasAssets = False
        self.symbol = 'LINKUSDT'
        self.short_ma = None
        self.long_ma = None
        
        self.separation = 0.0015

        # Trade info
        self.balance = 1000.00
        self.buy_price = 0.00
        self.sell_price = 0.00
        self.volume = 0
        self.profit = 0.00
        

        # Stop loss 
        self.stop_loss_price = 0
        self.stop_loss_amount = 0.01
        self.stop_loss_update_amount = 0.008

        # Timer stuff
        self.slow_update = 60
        self.fast_update = 10
        self.buy_last_update = time()
        self.sell_last_update = time()
        self.update_time_short = 0
        self.update_time_long = 0

        # Logging
        if(sys.platform == 'win32'):
            self.file_path = 'Logs\\VersionTwo\\' 
        elif(sys.platform == 'linux'):
            self.file_path = 'Logs/VersionTwo/'
        self.file_name = str(datetime.now().date())
        self.file_extension = '.txt'

        # Backtest
        self.backtest_file = 'Backtests\\LINKUSDT.csv'
        self.backtest_last_row = 30

    def update(self):
        # FIXME
        self.find_exit_point()
        self.find_entry_point()
        
    # Find when to buy  
    def find_entry_point(self ):
        if time() - self.buy_last_update >= self.slow_update - self.update_time_long:
            tt = time()
            self.get_candle_data()
            self.data = self.load_binance_data_from_csv()
            self.short_ma = self.data['Close'].rolling(window=7).mean()
            self.long_ma = self.data['Close'].rolling(window=25).mean()
           
            # Buy Coins
            if not self.hasAssets and self.short_ma[-1] > self.long_ma[-1] + self.separation and self.short_ma[-1] > self.short_ma[-2]:
                self.buy_coins()
                print('Buy order at {}'.format(self.buy_price))
                
            
            print(self.get_timestamp() + 'Canldes update')
            self.buy_last_update = time()
            self.update_time_long = time() - tt
    # Find when to sell curency
    def find_exit_point(self):
        if self.hasAssets and time() - self.sell_last_update >= self.fast_update - self.update_time_short:
            tt = time()
            current_price = self.get_price_data()

            # Sell Coins 
            if current_price < self.stop_loss_price or self.short_ma[-1] < self.short_ma[-2]:
                self.sell_coins(current_price)

            # Update Stop loss
            if current_price >= self.buy_price + self.stop_loss_update_amount:
                self.stop_loss_price = current_price - self.stop_loss_amount

            print(self.get_timestamp() + ' Sell update')
            self.sell_last_update = time()
            self.update_time_short = time() - tt
    # Get the current time 
    def get_timestamp(self):
        if self.mode == 0:
            timestamp = '[{0}:{1}:{2}] '.format(str(datetime.now().hour),str(datetime.now().minute), str(datetime.now().second))
            return timestamp
        else:
            return 'Backtest '
    # Get candle data and save it to a csv
    def get_candle_data(self):
        if self.mode is 0:
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
    # Get the current average price
    def get_price_data(self):
        if self.mode is 0:
            client = Client(Pkey, Skey)
            return self.truncate(client.get_avg_price(symbol=self.symbol)['price'], 4)
        elif self.mode is 1:
            with open(self.backtest_file, 'r') as f:
                lines = f.readlines()
                x = lines[self.backtest_last_row].split(',')
                c = rand.uniform(self.truncate(x[3], 4), self.truncate(x[2], 4))
                return self.truncate(c, 4)
    # Load data from a csv
    def load_binance_data_from_csv(self):
        if self.mode is  0:
            filename = 'CSV\\' + self.symbol + '.csv'
            with open(filename, 'r') as f:
                data = pd.read_csv(filename)
                data.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote asset volume', 
                'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume']
                data.set_index('Date', inplace=True)
                
                f.close()
                return data
        elif self.mode is 1:
            with open(self.backtest_file, 'r') as f:
                lines = f.readlines()
                data_list = []
                for i in range(self.backtest_last_row):
                    x = lines[i].split(',')
                    data_list.append(x)
                self.backtest_last_row += 1
                data = df(data_list)
                data.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote asset volume', 
                'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume']
                data.set_index('Date', inplace=True)
                return data             
    # Util function for truncating floats 
    def truncate(self,f, n):
        '''Truncates/pads a float f to n decimal places without rounding'''
        s = '{}'.format(f)
        if 'e' in s or 'E' in s:
            return '{0:.{1}f}'.format(f, n)
        i, p, d = s.partition('.')
        return float('.'.join([i, (d+'0'*n)[:n]]))
    # Log trade to file 
    def log_to_file(self):
        path = self.file_path + self.file_name + self.file_extension
        if os.path.exists(path):
           with open(path, 'a') as f:
               f.write('Trade symbol ' + str(self.symbol) + '\n')
               f.write('Buy price ' + str(self.buy_price) + '\n')
               f.write('Sell price ' + str(self.sell_price) + '\n')
               f.write('Volume ' + str(self.volume) + '\n')
               f.write('Profit ' + str(self.profit) + '\n')
               f.write('Current balance ' + str(self.truncate(self.balance,2)) + '\n\n')
               f.close()
        else:
            with open(path, 'w') as f:
                f.close()
                self.log_to_file()
    # Check is selected mode valid
    def validate_selected_mode(self, mode):
        if mode == 0 or mode == 1:
            return mode
        else:
            raise Exception('Invalid mode selceted ! \nmode 0 - live data \nmode 1 - backtest \nyou entered {}'.format(mode))
    
    def buy_coins(self):
        current_price = self.get_price_data()
        if self.balance > current_price:
            self.hasAssets = True
            self.buy_price = current_price
            self.calculate_volume(current_price)
            self.stop_loss_price = self.buy_price - self.stop_loss_amount
    
    def sell_coins(self, current_price):
        self.hasAssets = False
        self.sell_price = current_price
        sell_price = self.truncate((self.sell_price - (self.sell_price * 0.01)), 2 )
        self.balance += self.volume * sell_price
        self.profit = self.truncate((self.sell_price - self.buy_price) * self.volume, 2)
        print(self.get_timestamp() +'Sold at {0} with a profit of {1} \a'.format(self.sell_price, self.profit))
        self.log_to_file()
        self.buy_price = 0.00
        self.sell_price = 0.00
        self.volume = 0
        self.profit = 0.00

    def calculate_volume(self, price):
        volume = self.balance / price
        self.volume = int(volume)
        price = price + (price * 0.1)
        self.balance -= self.volume * price 

    

    def initialize_settings(self):
        filepath = 'Settings\\' + self.name + '.cfg'
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                pass
        else:
            pass

    def __get_setting_string(self, setting_name, setting_type, settings_file):
        pass