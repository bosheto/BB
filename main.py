from datetime import datetime
from dataB import get_binance_candle_data
from binance.client import Client
import time
from utils.logger import AI_Logger, Logger
from bot import Bot_AI, Bot_Daisy
rate = 1
from trader import Trader
last_update = datetime.now().minute

log = Logger()
ai_log = AI_Logger('Desy')
ai_log_n = AI_Logger('Daisy')
bot = Bot_AI('LINKUSDT', ai_log, 100)
bot_n = Bot_Daisy('LINKUSDT',ai_log_n)
def update():
    get_binance_candle_data('LINKUSDT', Client.KLINE_INTERVAL_1MINUTE, '1 minute ago UTC')
    log.add_line_to_log('Data downloaded ')
    bot.update()
    bot_n.update()
    log.add_line_to_log('Bots update')
    
t = Trader()

startup = False
upd_time = 0
last_tick = time.time()
#
get_binance_candle_data('LINKUSDT', Client.KLINE_INTERVAL_1MINUTE, '8 hours ago UTC')
while True:
    t.update()
    # if not startup and time.time() - last_tick >= 60 - upd_time:
    #     tt = time.time()
    #     update()
    #     upd_time = time.time()-tt
    #     last_tick = time.time()
        
        


   
        