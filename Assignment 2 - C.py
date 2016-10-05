# -*- coding: utf-8 -*-


import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


#Initial Values based on student numbers.
S1 = 332712 
S2 = 366515
S3 = 384825
S4 = 388049

np.random.seed(44)

c = int(repr(S1)[-1])/100
s_zero = round(5*(int(repr(S2)[-1])+int(repr(S3)[-1]))/2)
k = s_zero
vol = max(0.15, int(repr(S4)[-1])/20) 

#Black Scholes
def BS(s_bs,k_bs,r_bs,vol_bs,T_bs):
    d1 = (np.log(s_bs/k_bs)+(r_bs+0.5*vol_bs**2)*T_bs)/(vol_bs*np.sqrt(T_bs))
    d2 = (np.log(s_bs/k_bs)+(r_bs-0.5*vol_bs**2)*T_bs)/(vol_bs*np.sqrt(T_bs))
    bs_call_price = s_bs*stats.norm.cdf(d1)-k_bs*np.exp(-r_bs*T_bs)*stats.norm.cdf(d2)
    return bs_call_price
            


closed_price = s_zero*stats.norm.cdf((np.log(s_zero/k)+(0.5*vol*vol))/(vol), 0, 1)-k*stats.norm.cdf((np.log(s_zero/k)-(0.5*vol*vol)))

num_simulations = 1000000

e = np.random.normal(0, 1, num_simulations)
s_T = s_zero*np.exp(-0.5*np.square(vol)+vol*e)
price_call = np.fmax(s_T-k, 0)
print ("Mean Stock Price = ", np.mean(s_T))
print("BS call price=", BS(s_zero,k,0,vol,1))
print ("Call price = ", np.mean(price_call))
#Now with transaction costs

n = 250

vol_tc = np.sqrt(vol*(1+(2*c*np.sqrt(n))/vol))
s_T_tc = s_zero*np.exp(-0.5*np.square(vol_tc)+vol_tc*e)
price_call_tc = np.fmax(s_T_tc-k, 0)  
print("BS call price with tc=", BS(s_zero,k,0,vol_tc,1))
print ("Call price with tc = ", np.mean(price_call_tc))

#Exotic Option
price_exotic = s_T*((k-s_T)>0)
#for i in range(0, num_simulations):
#    if s_T[i] < k:
#        price_exotic[i] = s_T[i]
#    else:
#        price_exotic[i] = 0
#        
print ("Exotic price= ", np.mean(price_exotic))
    