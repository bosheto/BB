from dataB import load_binance_data_from_csv, get_binance_candle_data

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
    data = None
    mean_s = None
    mean_l = None
    hasAssets = False
    buy_price = 0
    sell_price = 0
    quantiti = 0
    uptrend = False
    logger = None
    stop_loss = 0
    stop_loss_percent = 0.2
    trade_data = {
        'symbol':'',
        'time':'',
        'buy price':0,
        'volume':0,
        'sell price':0,
        'profit':0,
        'profit %': 0,
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
        'profit %': 0,
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

        if self.data['Close'][-1] <= self.stop_loss:
            self.sell_coins('StopLoss')
            return

        if self.hasAssets and self.mean_s[-1] < self.mean_l[-1]:
            self.sell_coins('BottomOut')

        if self.hasAssets and self.mean_s[-1] > self.mean_s[-2]:
            self.stop_loss = self.data['Low'][-2] * (self.data['Low'][-2] * self.stop_loss_percent)

        if not self.hasAssets and self.mean_s[-1] > self.mean_l[-1] and self.mean_s[-1] > self.mean_s[-2]:
            self.buy_coins()
        
        if self.mean_s[-1] <= self.mean_s[-2] - 0.008 and self.hasAssets:
            self.sell_coins('AlgoOut')
            
    
    def buy_coins(self):
        self.hasAssets = True
        self.buy_price = self.data['Close'][-1]
        self.trade_data['time'] = str(datetime.now()) + '-'
        self.trade_data['buy price'] = self.buy_price
        self.stop_loss = self.buy_price -  (self.buy_price / self.stop_loss_percent)
        print('Bought at ' + str(self.buy_price))

    def sell_coins(self, flag):
        self.hasAssets = False
        self.sell_price = self.data['Close'][-1]
        self.recent_buy = True
        self.evaluate_trade(flag)
        self.logger.write_to_trade_file(self.trade_data)
        self.reset_trade_info()
        self.stop_loss = 0
        print('Sold at ' + str(self.sell_price))

    def evaluate_trade(self, flag):
        self.trade_data['flag'] = flag
        self.trade_data['time'] = self.trade_data['time'] + str(datetime.now())
        self.trade_data['sell price'] = self.sell_price
        self.trade_data['profit'] = self.sell_price - self.buy_price
        self.trade_data['profit %'] = ((self.sell_price - self.buy_price)/ self.buy_price) * 100 
        #self.logger.write_to_trade_file(self.trade_data)

    def reset_trade_info(self):
        self.trade_data = {
        'symbol':'',
        'time':'',
        'buy price':0,
        'volume':0,
        'sell price':0,
        'profit':0,
        'profit %': 0,
        'flag':''        
    }