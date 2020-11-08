import pandas

def MA(data_set, scale, color):
    moving_avg = data_set['Close'].rolling(window=scale).mean()
    return {
        'data': moving_avg,
        'scale': scale,
        'color': color
    }

def EMA(data_set, scale, color):
    dat = data_set.reindex(index=data_set.index[::-1])
    eMa = dat['Close'].ewm(span=scale, min_periods=0, adjust=False, ignore_na=False).mean()
    eMa = eMa.reindex(index=eMa.index[::-1])
    
    return {
        'data': eMa,
        'scale': scale,
        'color': color
    }