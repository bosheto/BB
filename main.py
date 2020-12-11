from datetime import datetime
from dataB import get_binance_candle_data
from binance.client import Client
import time
from utils.logger import AI_Logger, Logger
from bot import Bot_AI, Bot_Daisy
rate = 1
from trader import Trader
last_update = datetime.now().minute

t_link = Trader(symbol='LINKUSDT', bot_id=1, capital=700.00)
t_ada = Trader(symbol='ADAUSDT', bot_id=2, capital=300.00)

'''Convert hours to seconds'''
def hours_to_seconds(hours):
    return (60 * 60) * hours

startup = True
cicle_time = hours_to_seconds(6) 


print('Retrieving starting data')
get_binance_candle_data('LINKUSDT', Client.KLINE_INTERVAL_1MINUTE, '30 minutes ago UTC')
get_binance_candle_data('ADAUSDT', Client.KLINE_INTERVAL_1MINUTE, '30 minutes ago UTC')
print('Data retrieved. Starting:')

start_time = time.time()
while True:
    if startup and not datetime.now().second == 20:
        startup = False
        continue
    t_link.update()
    t_ada.update()
    if time.time() - start_time >= cicle_time:
        break

print('Cycle complete')

