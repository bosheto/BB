
from binance.enums import *
from time import time
from datetime import datetime
from pandas import DataFrame as df 
import pandas as pd
import os
from utils import get_proper_path, percent_change

class Trader:

    def __init__(self, data_retriever=None, symbol='',capital=0.00, mode=0, bot_id = None):
        # General stuff
        self.name = 'Trader'
        self.version = 'a1.3a'
        self.mode = self.validate_selected_mode(mode)
        self.data = None
        self.hasAssets = False
        self.symbol = symbol
        self.short_ma = None
        self.long_ma = None
        self.bot_id = bot_id
        self.separation = 0.05
        self.dt = data_retriever
        self.interval = KLINE_INTERVAL_1MINUTE


        # Trade info
        self.balance = capital
        self.buy_price = 0.00
        self.sell_price = 0.00
        self.volume = 0
        self.profit = 0.00
        self.buy_time = None
        self.sell_time = None

        # Stop loss 
        self.stop_loss_price = 0
        self.stop_loss_percent = 0.1
        self.stop_loss_update_amount = 0.15

        # Timer stuff
        self.slow_update = 60
        self.fast_update = 10
        self.buy_last_update = time()
        self.sell_last_update = time()
        self.update_time_short = 0
        self.update_time_long = 0

        # Logging
        self.file_path = get_proper_path(['Logs', ''])
        self.file_name = str(datetime.now().date())
        self.file_extension = '.txt'

        #Deprecated
        # Backtest
        self.backtest_file = 'CSV\\ADAUSDT.csv'
        self.backtest_last_row = 30

    def update(self):
        self.find_exit_point()
        self.find_entry_point()
        
    # Find when to buy  
    def find_entry_point(self ):
        if time() - self.buy_last_update >= self.slow_update - self.update_time_long:
            tt = time()
            # self.get_candle_data()
            # self.data = self.load_binance_data_from_csv()
            # self.short_ma = self.data['Close'].rolling(window=7).mean()
            # self.long_ma = self.data['Close'].rolling(window=25).mean()
           
            self.update_data()

            # Buy Coins
            if not self.hasAssets and self.short_ma[-1] > self.long_ma[-1] and percent_change(self.short_ma[-1], self.long_ma[-1]) >= self.separation   and self.short_ma[-1] > self.short_ma[-2]:
                self.buy_coins()
                print('Buy order {0} at {1}'.format(self.symbol, self.buy_price))
                
            
            log_str = self.get_timestamp() + 'Canldes update ' + self.symbol
            self.log_to_console(log_str)
            self.buy_last_update = time()
            self.update_time_long = time() - tt
    # Find when to sell curency
    def find_exit_point(self):
        if self.hasAssets and time() - self.sell_last_update >= self.fast_update - self.update_time_short:
            tt = time()
            current_price = self.dt.get_current_price(self.symbol)

            # Sell Coins 
            if current_price < self.stop_loss_price or self.short_ma[-1] < self.short_ma[-2]:
                self.sell_coins(current_price)
           
            
            # Update Stop loss
            if current_price >= self.stop_loss_price * (1 - self.stop_loss_update_amount):
                self.stop_loss_price = current_price * (1 - self.stop_loss_percent)

            print(self.get_timestamp() + ' Sell update ' + self.symbol )
            self.sell_last_update = time()
            self.update_time_short = time() - tt
    # Get the current time 
    def get_timestamp(self):
        if self.mode == 0 or self.mode is 2:
            timestamp = '[{0}:{1}:{2}] '.format(str(datetime.now().hour),str(datetime.now().minute), str(datetime.now().second))
            return timestamp
        else:
            return 'Backtest '
    
    def update_data(self):
        self.dt.get_candle_data(self.symbol,self.interval, '1 minute ago UTC', _folder_path=['CSV'])
        self.data = self.dt.load_csv_data(self.symbol, ['CSV'])
        self.short_ma = self.data['Close'].rolling(window=7).mean()
        self.long_ma =self.data['Close'].rolling(window=25).mean()

    
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
               f.write('{0}-{1}\n'.format(self.buy_time, self.sell_time))
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
    # FIXME remove this
    # Check is selected mode valid
    def validate_selected_mode(self, mode):
        if mode == 0 or mode == 1 or mode == 2:
            return mode
        else:
            raise Exception('Invalid mode selceted ! \nmode 0 - live data \nmode 1 - backtest \nyou entered {}'.format(mode))
    
    def buy_coins(self):
        current_price = self.dt.get_current_price(self.symbol)
        current_price += current_price * 0.01
        if self.balance > current_price:
            self.hasAssets = True
            self.buy_price = current_price
            self.calculate_volume(current_price)
            self.stop_loss_price = self.buy_price  * (1.0 - self.stop_loss_percent)
            self.buy_time = self.get_timestamp()

    def sell_coins(self, current_price):
        self.hasAssets = False
        self.sell_price = current_price
        sell_price = current_price + (current_price * 0.01)
        self.balance += (self.volume * sell_price) 
        self.profit = self.truncate((self.sell_price - self.buy_price) * self.volume, 2)
        self.sell_time = self.get_timestamp()
        print(self.get_timestamp() +'Sold {2} at {0} with a profit of {1} \a'.format(self.sell_price, self.profit, self.symbol))
        self.log_to_file()
        self.buy_price = 0.00
        self.sell_price = 0.00
        self.volume = 0
        self.profit = 0.00

    def calculate_volume(self, price):
        volume = self.balance / price
        self.volume = int(volume) 
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

    def log_to_console(self, string, print_last_ma=True):
        
        print(string)
        

   
class TradeData:

    def __init__(self):
        self.buy_price = 0
        self.sell_price = 0
        self.stop_losses = []
        self.buy_time = None
        self.sell_time = None
    

    def debug(self):
        print('Buy Price')
        print(self.buy_price)
        print('\nSell Price')
        print(self.sell_price)
        print('\nStop loss amounts')
        for i in self.stop_losses:
            print(i)
        print('\nBuy Time')
        print(self.buy_time)
        print('\nSell Time')
        print(self.sell_time)

