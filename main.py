from datetime import datetime
from dataB import get_binance_candle_data
from binance.client import Client
import time
from utils.logger import AI_Logger, Logger
from bot import Bot_AI, Bot_Daisy
rate = 1
from trader import Trader
last_update = datetime.now().minute

t = Trader()

'''Convert hours to seconds'''
def hours_to_seconds(hours):
    return (60 * 60) * hours

startup = True
cicle_time = hours_to_seconds(16) 


print('Retrieving starting data')
get_binance_candle_data('LINKUSDT', Client.KLINE_INTERVAL_1MINUTE, '30 minutes ago UTC')
print('Data retrieved. Starting:')

start_time = time.time()
while True:
    if startup and not datetime.now().second == 20:
        continue
    t.update()
    if time.time() - start_time >= cicle_time:
        break

print('Cycle complete')

