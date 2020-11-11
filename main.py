from datetime import datetime
from dataB import get_binance_candle_data
from binance.client import Client

rate = 1

last_update = datetime.now().minute

def update():
    get_binance_candle_data('LINKUSDT', Client.KLINE_INTERVAL_1MINUTE, '1 minutes ago UTC')
    print('Update \n')
    
current_minute = 0


while True:
    time = datetime.now()
    current_minute = time.minute

    if current_minute - rate >= last_update:  
        update()
        last_update = current_minute
        isZeroMin = False
    
    if current_minute - rate == -rate and not isZeroMin:
        update()
        isZeroMin = True
        