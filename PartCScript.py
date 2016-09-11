# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 11:54:43 2016

@author: ms
"""
import math
s  = 60
su = 80
sd = 40
pu = 10
pd = 50
 
k = 90
r = .05

current = k-s 
future  = (pu-pd)/(su-sd)*s+math.exp(-r)*(pu-su*(pu-pd)/(su-sd))

print('stock: {}'.format((pu-pd)/(su-sd)))
print('bonds: {}'.format(math.exp(-r)*(pu-su*(pu-pd)/(su-sd))))

print(current)
print(future)
print(max(current, future))