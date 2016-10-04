# -*- coding: utf-8 -*-
"""
Created on Sat Sep 27 9:36:57 2016

@author: LARO
"""

import numpy as np
from scipy.stats import norm

# This code will calculate the price of an European call option.


#initialisation
c = 0.02    #Transaction costs
S0 = 25     #Initial stock price
K = 25      #Strike price
vol = 0.45  #Volatility of the stock price
mu = 0      #Drift
r = 0       #Interest rate
B = 1       #Bond price
R = 1000000 #Amount of simulations
T = 1       #End period, in this case 1 year. 
S = np.empty([1,R])
X = np.empty([1,R])
V = np.empty([1,R])
np.random.seed(44)
n = 250     # will be the number of readjustments  because we hold the stock a year
            # and it will be continuous time, every trading day (250 per year)
            # the self-financing portfolio will be readjusted in order to mimic 
            # the claim.
#%% regular call with Black Scholes model

vol_tilde = np.sqrt(vol*(1+(2*c*np.sqrt(n))/(vol*np.sqrt(T)))) 

#For the case where the transaction costs are taken into account change all the vol's in the next LOC
#into vol_tilde.

for i in range(0,R):
    S[0,i]= S0*np.exp((r-(np.square(vol))/2)*T +vol*np.sqrt(T)*np.random.normal(0,1))
    X[0,i] = np.maximum((S[0,i]-K),0)
    V[0,i] = np.exp(-r*T)*X[0,i]
Vhat = np.mean(V)
print(Vhat)

# analytical closed form expression of the Black Scholes model
part1 =  S0*norm.cdf((np.log(S0/K) + (r + 0.5*(np.power(vol,2))*T))/(vol*np.sqrt(T)))
part2 = K*np.exp((-r*T))*norm.cdf((np.log(S0/K)+ (r - 0.5*(np.power(vol,2))*T))/(vol*np.sqrt(T))) 
V_ana = part1-part2
print(V_ana)

#%% In case of the new exotic priced derivative

for i in range(0,R):
    S[0,i]= S0*np.exp((r-(np.square(vol))/2)*T +vol*np.sqrt(T)*np.random.normal(0,1))
    if (S[0,i]-K) <0:
        X[0,i] = S[0,i]
    else:
        X[0,i] = 0
    V[0,i] = np.exp(-r*T)*X[0,i]
Vhat = np.mean(V)
print(Vhat)

# analytical closed form expression of the Black Scholes model when pricing an Asset-or-Nothing put
V_ana = S0*np.exp(-r*T)*norm.cdf(-((np.log(S0/K) + (r+0.5*vol**2)*T)/(vol*np.sqrt(T))))
print(V_ana)
