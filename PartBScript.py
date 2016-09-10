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



xls = pd.ExcelFile('Crude Oil - Gold Data.xls')
goldfut = xls.parse('Gold')
cofut = xls.parse('Crude oil')

cofut.plot(x='Date', y='Price')
daily_vol = cofut.std()
maintenance = st.norm.ppf(.99)*np.sqrt(3)*daily_vol

