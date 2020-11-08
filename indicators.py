import pandas

def MovingAverage(data_set, scale, color):
    moving_avg = data_set['Close'].rolling(window=scale).mean()
    return {
        'data': moving_avg,
        'scale': scale,
        'color': color
    }

