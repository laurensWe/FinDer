# -*- coding: utf-8 -*-

import pandas as pd
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

