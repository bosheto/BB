from dataB import get_binance_candle_data
from binance.enums import *
from indicators import MA
import time

coins_to_track = ['ADAUSDT', 'LINKUSDT', 'LINKUPUSDT', 'LINKDOWNUSDT']
interval = KLINE_INTERVAL_1MINUTE
from_time = '24 hours ago UTC'
update_time = 60

def track():
    for coin in coins_to_track:
        data = get_binance_candle_data(coin, interval, from_time)
        mean_s = MA(data, 7, 'purple')['data']
        mean_l = MA(data, 20, 'red')['data']
        if mean_s[-1] > mean_l[-1]:
            print('True for {}'.format(coin))


t = time.time()

# while True:
#     nt = time.time()
#     if nt - t >= update_time:
#         print('Update')
#         track()
#         t = time.time()


def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])





print(float(truncate(1.23456754, 4)))