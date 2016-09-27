# -*- coding: utf-8 -*-


import numpy as np


#Initial Values based on student numbers.
S1 = 332712 
S2 = 366515
S3 = 384825
S4 = 388049

c = int(repr(S1)[-1])/100
s_zero = round(5*(int(repr(S2)[-1])+int(repr(S3)[-1]))/2)
k = s_zero
vol = max(0.15, int(repr(S4)[-1])/20) 

num_simulations = 1000000

e = np.random.normal(0, 1, num_simulations)
s_T = s_zero*np.exp(-0.5*np.square(vol)+vol*e)
price_call = np.fmax(s_T-k, 0)
print ("Mean Stock Price = ", np.mean(s_T))
print ("Call price = ", np.mean(price_call))
#Now with transaction costs

n = 250

vol_tc = np.sqrt(vol*(1+(2*c*np.sqrt(n))/vol))
s_T_tc = s_zero*np.exp(-0.5*np.square(vol_tc)+vol_tc*e)
price_call_tc = np.fmax(s_T_tc-k, 0)  
print ("Call price with tc = ", np.mean(price_call_tc))