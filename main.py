from datetime import datetime
from dataB import get_binance_candle_data
from binance.client import Client
import time
from utils.logger import AI_Logger, Logger
from bot import Bot_AI
rate = 1

last_update = datetime.now().minute

log = Logger()
ai_log = AI_Logger('Desy')
bot = Bot_AI('LINKUSDT', ai_log)

def update():
    get_binance_candle_data('LINKUSDT', Client.KLINE_INTERVAL_1MINUTE, '1 minute ago UTC')
    log.add_line_to_log('Data donwloaded ')
    bot.update()
    log.add_line_to_log('Bot update')
    
    
startup = True

#get_binance_candle_data('LINKUSDT', Client.KLINE_INTERVAL_15MINUTE, '24 hours ago UTC')
while True:
    if startup and datetime.now().second == 7:
        startup = False
    if not startup:
        start_time = time.time()
        update()
        end_time = time.time() - start_time
        time.sleep(60 - end_time)


   
        