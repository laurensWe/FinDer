 # -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 09:44:10 2016

This program is for the assignment set of financial derivatives Part B, where a simulation of an portfolio of futures will be executed.

@author: LARO
"""

" Quanld Part "
##import quandl

## WheatData = quandl.get("CHRIS/CME_W1", ticker='AAPL')
## df = WheatData.loc['2013-01-01':'2016-09-02', 'Open']

## df.plot()


"Excel Part"

import pandas as pd
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt

xls = pd.ExcelFile('Crude Oil - Gold Data.xls')
goldfut = xls.parse('Gold')
cofut = xls.parse('Crude oil')

#names = cofut.columns.tolist()
#names[names.index('Price')] = 'Crude Oil Future Price (in dollar)'
#cofut.columns = names

#cofut.plot(x='Date', y='Price')
daily_vol = cofut.std()
maintenance = st.norm.ppf(.99)*np.sqrt(3)*daily_vol

cofut['Change'] =cofut['Price'].diff()

#%%
" This piece of code does the simulation of the margin account"

#initialisation
InitialAc = 98120
MainteReq = 73590
AmountMarginCalls = 0
retrieve = 0
Margin = [98120]
MarginExcess = [98120]
Difference = [0]
ContractSize = 1000

initialIndex = 648

for num in range(initialIndex,initialIndex + 105):  #648 is the index for 2008-09-02 and 754 is the index for 2009-02-02
    DiffMargin = cofut['Change'][num+1] * ContractSize
    Difference.append(DiffMargin)
    tempMargin = Margin[num - initialIndex] + DiffMargin
    
    if tempMargin < MainteReq:
        MarginExcess.append(tempMargin)
        AmountMarginCalls = AmountMarginCalls + 1
        Margin.append(InitialAc)   # if the maintenance requirement has been reached, the margin account should be filled to the initial margin value.
    elif tempMargin > InitialAc:
        MarginExcess.append(tempMargin)        
        Margin.append(InitialAc)   # If the Max (Initial Margin) has been reached, the money will be deposited on your account.
        retrieve = retrieve + 1
    else:
        Margin.append(tempMargin)
        MarginExcess.append(tempMargin)
        
MarginExcess2 = pd.DataFrame(MarginExcess, columns=['Data'])
MarginExcess2['Date'] = 1
for num in range(initialIndex,initialIndex + 106):
    MarginExcess2['Date'][num-648] = np.datetime64(cofut['Date'][num])

#%% Mooie plotjes van de Margin Account
#pd.DataFrame(Margin).plot()
#pd.DataFrame(MarginExcess).plot()
#t = linspace(MainteReq,MainteReq,106)
MarginExcess2.plot(x='Date',y='Data',label='Margin Account level')
plt.plot(MarginExcess2)
plt.ylabel('Level of the Margin Account (in $)')
plt.xlabel('Date of time (daily)')
plt.axhline(y=InitialAc, color='r',label='Initial Account')
plt.axhline(y=MainteReq, color='r',label='Maintenance Requirement')
plt.ylim(ymin=65000 ,ymax=105000) 
    
