# -*- coding: utf-8 -*-
"""
Created on Sat Sep 27 9:36:57 2016

@author: LARO
"""
import math
import pandas as pd
import numpy as np

# This code will calculate the price of an European call option.


#initialisation
c = 0.02    #Transaction costs
S0 = 25     #Initial stock price
K = 25      #Strike price
vol = 0.45  #Volatility of the stock price
mu = 0      #Drift
r = 0       #Interest rate
B = 1       #Bond price
R = 100000    #Amount of simulations
T = 1       #End period, in this case 1 year. 
S = np.empty([1,1000])
X = np.empty([1,1000])
V = np.empty([1,1000])

for i in range(0,1000):
    S[0,i]= S0*np.exp((r-(np.square(vol))/2)*T +vol*np.sqrt(T)*np.random.normal(0,1))
    X[0,i] = np.maximum((S[0,i]-K),0)
    V[0,i] = np.exp(-r*T)*X[0,i]
Vhat = np.mean(V)
print(Vhat)

