from datetime import datetime
from dataB import get_binance_candle_data
from binance.client import Client
import time
from utils.logger import AI_Logger, Logger
from bot import Bot_AI
log = Logger()
ai_log = AI_Logger('test')
bot = Bot_AI('BNBUSDT', ai_log)


start_time = time.time()
get_binance_candle_data('BNBUSDT', Client.KLINE_INTERVAL_1MINUTE, '1 minute ago UTC')
bot.update()
log.add_line_to_log('test')
log.add_line_to_log('test')
endtime = time.time() - start_time

print(endtime)