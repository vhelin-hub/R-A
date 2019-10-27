# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 18:29:54 2019

@author: Yasser
"""

import numpy as np
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt 
import pandas as pd

#%%
data=pd.read_hdf('20180801_20190201_EURUSD.h5')

#%%

data_5min= data.resample('5T').mean().dropna()

#%%

twenty18_September_fifth= data_5min['2018']['bid']
#twenty18_September_fifth.plot()

max_idx=list(argrelextrema(twenty18_September_fifth.values,np.greater, order=7)[0])
min_idx=list(argrelextrema(twenty18_September_fifth.values,np.less, order=7)[0])
    
idx= max_idx+min_idx 
idx.sort()
    
peaks= twenty18_September_fifth.values[idx]

Bullish_Impulse=[]

error_range= 5.0/100


for i in range(len(idx)):
    if len(idx[i:i+4]) == 4:
        
        window=idx[i:i+4]
        
        a, b, c, d = twenty18_September_fifth[window].values
        
        bc_range= np.array([0.618 - error_range, 0.786 + error_range]) * abs(a-b)
        cd_range= np.array([1.272 - error_range, 1.618 + error_range]) * abs(b-c)
        
        if  a > b and b < c and d < c:
            if bc_range[0] < abs(b-c) < bc_range[1] and cd_range[0] < abs(c-d) < cd_range[1] and abs(a-b)*0.9 < abs(c-d) < abs(a-b)*1.1:
                Bullish_Impulse.append(window)
    else:
        break
    
plt.figure(1)
plt.plot(twenty18_September_fifth.index,twenty18_September_fifth.values, color='b')
#plt.plot(twenty18_September_fifth.index[idx],twenty18_September_fifth.values[idx],linewidth=2, color='k')
plt.scatter(twenty18_September_fifth.index[idx],twenty18_September_fifth.values[idx],linewidth=5, color='orange')
for i in range(len(Bullish_Impulse)):
    plt.plot(twenty18_September_fifth.index[Bullish_Impulse[i]],twenty18_September_fifth.values[Bullish_Impulse[i]],linewidth=7, color= 'orange')
plt.show()


