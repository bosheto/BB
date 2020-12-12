from datetime import datetime
from dataB import get_binance_candle_data
from binance.client import Client
import time
rate = 1
from trader import Trader
last_update = datetime.now().minute
import argparse 

parser = argparse.ArgumentParser()
parser.add_argument('--symbol', dest='symbol', help='symbol to trade', type=str)
parser.add_argument('--capital',dest='capital', help='Starting capital', type=float)
parser.add_argument('--cycle', dest='cycle', help='Cycle time', type=int)
args = parser.parse_args()

bot = Trader(symbol=args.symbol, capital=args.capital, mode=0, bot_id=1)

'''Convert hours to seconds'''
def hours_to_seconds(hours):
    return (60 * 60) * hours

startup = True

cicle_time = hours_to_seconds(args.cycle) 


print('Retrieving starting data')
get_binance_candle_data(args.symbol, Client.KLINE_INTERVAL_1MINUTE, '30 minutes ago UTC')
print('Data retrieved. Starting:')

start_time = time.time()

while True:
    if startup and not datetime.now().second == 7:
        startup = False
        continue
    bot.update()
    
    if time.time() - start_time >= cicle_time:
        break

print('Cycle complete')