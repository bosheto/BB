 
import pandas as pd 
import numpy as np
import math
import datetime

tolerance = 0.0008

def find_exit_point(data):
    c = 0
    for i in range(len(data)):
        if i == 0:
            continue

        v = data[1]
        t = data[0]
        # if t[i].hour < 19 and t[i].minute < 52:
        #     continue
        if v[i] < v[i-1]:
            if (v[i] + tolerance) - v[i-1] < 0:
            #to = datetime.datetime.fromtimestamp(t[i])
                print(t[i])
                break

    print(c)

        


def find_entry_point(data, indicator_1, indicator_2):

    df = pd.DataFrame(data)
    df['MA_short'] = indicator_1
    df['MA_long'] = indicator_2
    s = df['MA_short']
    l = df['MA_long']  

    pl_data = []

    for i in range(len(df)):
        #print(str(s[i]) + ' : ' + str(s.index[i]))
        if not np.isnan(s[i]) and not np.isnan(l[i]):    
            if s[i] > l[i]:
                out_l =[]
                out_l.append(df.index[i])
                out_l.append(s[i])
                pl_data.append(out_l)

    tf = pd.DataFrame(pl_data)
    #find_exit_point(tf)


def golden_cross(data, indicator_1, indicator_2):
    
    df = pd.DataFrame(data)
    df['MA_short'] = indicator_1
    df['MA_long'] = indicator_2
    s = df['MA_short']
    l = df['MA_long']  
    p = df['Close']
    ep = []
    sp = []
    entry_position = None
    exit_position = None


    for i in range(len(df)):
        
        if s[i] > l[i] and entry_position is None:
            ep.append(s[i])
            entry_position = p[i] 
            continue
        elif s[i] < l[i] and entry_position != None:
            entry_position = None
                        
        ep.append(np.nan)
    return ep
        

def sell_point(data, indicator_1, indicator_2):
    df = pd.DataFrame(data)
    df['MA_short'] = indicator_1
    df['MA_long'] = indicator_2
    s = df['MA_short']
    l = df['MA_long']  
    p = df['Close']
