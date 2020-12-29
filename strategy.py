
from utils import get_percent_change

class GoldenCross:

    def __init__(self, client, symbol, capital, stop_loss_amount, stop_loss_update_amount, mas, mal, separation):
        self.symbol = symbol
        self.capital = capital
        self.stop_loss_amount = stop_loss_amount
        self.stop_loss_update_amount = stop_loss_update_amount
        self.ma_short = mas
        self.ma_long = mal
        self.separation = separation
        self.stop_loss_price = 0
        self.client = client

    #FIXME implement buy coins
    def slow_update(self, hasAssets, data):
        if not hasAssets and data[self.ma_short][-1] > data[self.ma_long][-1] and percent_change(data[self.ma_short][-1],data[self.ma_long][-1]) >= self.separation and data[self.ma_short][-1] > data[self.ma_short][-2]:
            
            #print('Buy at {}'.format())
            return True
    #FIXME implement sell coins
    def fast_update(self, hasAssets, current_price, data):
        if hasAssets and current_price < self.stop_loss_price or hasAssets and data[self.ma_short][-1] < data[self.ma_short][-2]:
            
            pass

    def buy_coins(self):
        pass

    def sell_coins(self):
        pass


    def __short_above_long(self):
        pass


class TradeData:

    def __init__(self):
        self.buy_price = 0.0
        self.sell_price = 0.0
        self.buy_time = None
        self.sell_time = None
        self.stop_loss = []
        self.flag = ''
    
    