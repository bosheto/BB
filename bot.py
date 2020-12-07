from dataB import load_binance_data_from_csv, get_binance_candle_data, get_current_price

from indicators import MA
from strategy import golden_cross
#from ploter import create_debug_chart
from binance.client import Client
from datetime import datetime
# data = get_binance_candle_data('BNBUSDT', Client.KLINE_INTERVAL_5MINUTE, '24 hours ago UTC')
# #data = load_binance_data_from_csv('BNBUSDT')
# mean = MA(data, 7, 'purple')
# mean_long = MA(data, 25, 'orange')

# t = golden_cross(data, mean['data'], mean_long['data'])

# create_debug_chart(data, [mean, mean_long], t[0], t[1])


class Bot_AI:
    
    symbol = ''
    name = 'Desy_0.1'
    data = None
    mean_s = None
    mean_l = None
    hasAssets = False
    buy_price = 0
    sell_price = 0
    quantiti = 0
    trend_backcheck = 5
    trend = 0
    logger = None
    stop_loss = 0
    stop_loss_percent = 0.05
    separation = 0.0123
    out_dif = 0.0004
    pref_profit = 0.04
    capital = 0
    profit_percent = 0.05
    trade_data = {
        'symbol':'',
        'time':'',
        'buy price':0,
        'volume':0,
        'sell price':0,
        'profit':0,
        'gain %': 0,
        'flag':''        
    }


    def __init__(self, symbol, logger, capital):
        self.symbol = symbol
        self.logger = logger
        self.capital = capital
        self.trade_data = {
        'symbol':'',
        'time':'',
        'buy price':0,
        'volume':0,
        'sell price':0,
        'profit':0,
        'gain %': 0,
        'flag':''        
        }

    def load_data(self):
        self.data = load_binance_data_from_csv(self.symbol)
        self.calculate_ma()

    def dump(self):
        print(self.mean_s.tail(10))
        print(self.mean_l.tail(10))
    
    def calculate_ma(self):
        ms = MA(self.data, 7, 'purple')
        self.mean_s = ms['data']
        ml = MA(self.data, 25, 'orange')
        self.mean_l = ml['data']

    def update(self):
        self.load_data()
        
        # if self.data['Close'][-1] <= self.stop_loss:
        #     self.sell_coins('StopLoss')
        #     return
        # # # if self.hasAssets and self.mean_s[-1] > self.mean_s[-2]:
        # # #     self.stop_loss = self.data['Close'][-2] - (self.data['Close'][-2] * self.stop_loss_percent)

        # if self.hasAssets and self.data['Close'][-1] > self.stop_loss and self.mean_s[-1] > self.mean_s[-2]:
        #     self.stop_loss = self.data['Close'][-1] - (self.data['Close'][-1] * self.stop_loss_percent)

        # if self.hasAssets and self.mean_s[-1] <= self.mean_l[-1]:
        #     self.sell_coins('BottomOut')

        # if self.mean_s[-1] <= self.mean_s[-2] - self.out_dif and self.hasAssets:
        #     self.sell_coins('AlgoOut')
        
        # if self.check_trend:
        #     # Find buy point
        #     if not self.hasAssets and self.mean_s[-1] > self.mean_l[-1] and self.mean_s[-1] > self.mean_s[-2] and (self.mean_s[-1] - self.mean_l[-1]) >= self.separation:
        #         self.buy_coins()
        self.update_stop_loss()
        if self.hasAssets and self.data['Close'][-1] < self.stop_loss:
            self.sell_coins('StopLoss')
        
        if self.hasAssets and self.mean_s[-1] < self.mean_s[-2]:
            self.sell_coins('MeanDown')
        
        if not self.hasAssets and self.mean_s[-1] > self.mean_l[-1] and self.mean_s[-1] > self.mean_s[-2]:
            self.buy_coins()

    def update_stop_loss(self):
        if self.hasAssets and self.data['Close'][-1] - 0.0004 > self.stop_loss:
            self.stop_loss = self.data['Close'][-1] - 0.0004


    def check_trend(self):
        if self.mean_l[-1] > self.mean_l[-2]:
            return True            
        else:
            return False
    def buy_coins(self):
        self.hasAssets = True
        self.buy_price = self.data['Close'][-1]
        self.trade_data['time'] = str(datetime.now()) + '-'
        self.trade_data['buy price'] = self.buy_price
        self.stop_loss = self.buy_price - 0.0004
        print(self.name + ' Bought at ' + str(self.buy_price))

    def sell_coins(self, flag):
        self.hasAssets = False
        self.sell_price = self.data['Close'][-1]
        self.recent_buy = True
        self.evaluate_trade(flag)
        self.logger.write_to_trade_file(self.trade_data)
        self.reset_trade_info()
        self.stop_loss = 0
        print(self.name + ' Sold at ' + str(self.sell_price))

    def evaluate_trade(self, flag):
        self.trade_data['flag'] = flag
        self.trade_data['time'] = self.trade_data['time'] + str(datetime.now())
        self.trade_data['sell price'] = self.sell_price
        self.trade_data['profit'] = self.sell_price - self.buy_price
        self.trade_data['gain %'] = ((self.sell_price - self.buy_price)/ self.buy_price) * 100 
        #self.logger.write_to_trade_file(self.trade_data)

    def reset_trade_info(self):
        self.trade_data = {
        'symbol':'',
        'time':'',
        'buy price':0,
        'volume':0,
        'sell price':0,
        'profit':0,
        'gain %': 0,
        'flag':''        
    }

    def fast_update(self):
        if self.hasAssets:
            if get_current_price(self.symbol) < self.stop_loss:
                self.sell_coins('StopLoss')
        else:
            return 


class Bot_Daisy:

    buy_signal = False

    name = 'Daisy'
    target_profit = 0.3
    symbol = ''
    signal_bar = None
    data = None
    mean = None
    stop_buy = 0
    hasAssets = False
    buy_price = 0
    sell_price = 0
    quantiti = 0
    uptrend = False
    logger = None
    stop_loss = 0
    stop_loss_modifier = 0.0004
    trade_data = {
        'symbol':'',
        'time':'',
        'buy price':0,
        'volume':0,
        'sell price':0,
        'profit':0,
        'gain %': 0,
        'flag':''        
    }


    def __init__(self, symbol, logger):
        self.symbol = symbol
        self.logger = logger
        self.trade_data = {
        'symbol':'',
        'time':'',
        'buy price':0,
        'volume':0,
        'sell price':0,
        'profit':0,
        'gain %': 0,
        'flag':''        
        }

    def load_data(self):
        self.data = load_binance_data_from_csv(self.symbol)
        self.calculate_ma()

    def calculate_ma(self):
        ms = MA(self.data, 20, 'purple')
        self.mean = ms['data']

    def update(self):
        
        try:
            self.load_data()
            self.find_signal_bar()
            self.find_buy_bar()
            if self.data[''] >= self.stop_loss:
                self.sell_coins('StopLoss')
        except:
            pass
        

        

        # if self.data['Close'][-1] <= self.stop_loss:
        #     self.sell_coins('StopLoss')
        #     return

        
        
        # if self.data['High'][-1] > self.mean[-1] and self.signal_bar == None:
        #     self.signal_bar = self.data['High'][-1]
         
        # if self.signal_bar != None and self.data['Open'][-1] > self.signal_bar:
        #     self.stop_buy = self.data['Low'][-1] - 0.0004
        #     self.buy_coins()

        # if self.mean[-1] > self.mean[-2]:
        #     self.stop_loss = self.data['Low'][-1] - 0.0004

    def find_buy_bar(self):
        if self.signal_bar != None and not self.hasAssets and self.data['Close'][-1] > self.signal_bar['High']:
            self.stop_loss = self.data['Low'][-1] - self.stop_loss_modifier
            self.buy_coins()

    def find_signal_bar(self):
        if self.buy_signal is False and self.data['High'][-1] > self.mean[-1] and self.signal_bar == None:
            self.buy_signal = True 
            self.signal_bar = self.data.tail(1)



    def calculate_stop_loss(self):
       pass 

    def buy_coins(self):
        self.hasAssets = True
        self.buy_price = self.data['Open']
        self.trade_data['time'] = str(datetime.now()) + '-'
        self.trade_data['buy price'] = self.buy_price
        #self.stop_loss = self.buy_price -  (self.buy_price * self.stop_loss_percent)
        print(self.name +' Bought at ' + str(self.buy_price))

    def sell_coins(self, flag):
        self.hasAssets = False
        self.signal_bar = None
        self.sell_price = self.data['Close'][-1]
        self.recent_buy = True
        self.evaluate_trade(flag)
        self.logger.write_to_trade_file(self.trade_data)
        self.reset_trade_info()
        self.stop_loss = 0
        print(self.name +' Sold at ' + str(self.sell_price))

    def evaluate_trade(self, flag):
        self.trade_data['flag'] = flag
        self.trade_data['time'] = self.trade_data['time'] + str(datetime.now())
        self.trade_data['sell price'] = self.sell_price
        self.trade_data['profit'] = self.sell_price - self.buy_price
        self.trade_data['gain %'] = ((self.sell_price - self.buy_price)/ self.buy_price) * 100 

    def reset_trade_info(self):
        self.trade_data = {
        'symbol':'',
        'time':'',
        'buy price':0,
        'volume':0,
        'sell price':0,
        'profit':0,
        'gain %': 0,
        'flag':''        
    }