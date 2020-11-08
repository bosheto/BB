 
import pandas as pd 
import numpy as np
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
    print(tf)    

