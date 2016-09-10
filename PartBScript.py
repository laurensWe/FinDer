 # -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 09:44:10 2016

This program is for the assignment set of financial derivatives Part B, where a simulation of an portfolio of futures will be executed.

@author: LARO
"""

import quandl
import numpy as np

WheatData = quandl.get("CHRIS/CME_W5", ticker='AAPL')
df = WheatData.loc['2013-01-01':'2016-09-02', 'Open']

df.plot()
