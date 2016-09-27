# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 09:17:04 2016

@author: ms
"""
import numpy as np
S1 = 2 # 332712 - Max Dubber
S2 = 5 # 366515 - Laurens Weijs
S3 = 5 # 384825 - Jinchen Li
S4 = 9 # 388049 - Sebastiaan Vermeulen
S0 = K = round(5*(S2+S3)/2)
c = S1/100
sigma = max(0.15, S4/20)

def recursivePrice(K,r=0,kind='E',pc='C'):
    fun = lambda Pu,Pd,Su,Sd,S: (S-np.exp(-r)*Su)*(Pu-Pd)/(Su-Sd)+np.exp(-r)*Pu
    if kind=='E':
        return fun
    elif kind=='A' and pc=='P':
        return lambda Pu,Pd,Su,Sd,S: max(K-S,fun(Pu,Pd,Su,Sd,S))
    else:
        return lambda Pu,Pd,Su,Sd,S: max(S-K,fun(Pu,Pd,Su,Sd,S))
        
def finalPrice(K, pc='P'):
    return lambda S: max(0,K-S) if pc=='P' else lambda S:max(0,S-K)
 
def assetTree(S,mu,sigma,N):
    price = lambda u,d: S*np.exp(mu*(u+d)+sigma*np.sqrt(u)-sigma*np.sqrt(d))
    return [[price(t-i,i) for i in range(t+1)] for t in range(N+1)]
    
def deepMap(fun,vec):
    return [*map(lambda x: [*map(fun,x)],vec)]
    
def tree(S,K,sigma,mu=0,N=1,r=0,kind='E',pc='P'):
    # inits of asset and option trees
    asset = assetTree(S,mu,sigma,N)
    option = [[] for i in range(N+1)]
    # option trees final values
    option[-1].extend([finalPrice(K,pc)(S) for S in asset[-1]])
    # recur through the option tree
    for i in range(N,0,-1):
        recur = recursivePrice(r,K,kind,pc)
        zipped = zip(option[i][1:],option[i][:-1],asset[i][1:],asset[i][:-1],asset[i-1])
        option[i-1].extend([recur(Pu,Pd,Su,Sd,S) for Pu,Pd,Su,Sd,S in zipped])
    # finalize and return
    deepRound = lambda y: deepMap(lambda x: round(x,2),y)
    return [deepRound(asset),deepRound(option)]
        
def printTree(tree):
    for line in tree:
        print('     '*(len(tree)-len(line)),end='')
        print(*map('{:9.2f}'.format, line))        
        
if __name__=='__main__':
    asset, option = tree(S0, K, sigma, N=4)
    printTree(asset)
    print('\n\n')
    printTree(option)
     

'''
#------------------------------------------------------------------------------
def european_tree(spot,strike,N,up,r,option_type):
    asset = lambda n:[spot*pow(up,n-i)*pow(down,i) for i in range(n+1)]
    option = []

        # calculate terminal call price
    if option_type == 'call': # call option
        option.append(list(map(lambda s:s-strike if (s-strike>0) else 0,asset(N))))
    else: # put option
        option.append(list(map(lambda s:strike-s if (strike-s>0) else 0,asset(N))))
        
        # determine recursion type
    recursion = lambda x:(p*x[0]+(1-p)*x[1])/r
    
        # calculate all option values recursively for all n=0,..,N-1
    for n in range(N-1,-1,-1):
        option.append([ recursion(x) for x in zip(option[-1][:-1],option[-1][1:])])

        # sort option list in ascending time
    option.reverse()
    
        # return option price tree
    return option

def american_tree(spot,strike,N,up,r,option_type):
        # all possible asset prices at time t, sorted high-low.
    asset = lambda n:[spot*pow(up,n-i)*pow(down,i) for i in range(n+1)]

    option = []    
   
       # set profit function according to option type
    if option_type == 'call': # call option
        f = lambda s: s-strike
    else: # put option
        f = lambda s: strike-s
      
        # calculate terminal call price
    option.append(list(map(lambda s:f(s) if (f(s)>0) else 0,asset(N))))
    
        # determine recursion type
    maximum = lambda x:max( ( p*x[0] + (1-p)*x[1] )/r , f(x[2]) )

        # calculate all option values recursively for all n=0,..,N-1
    for n in range(N-1,-1,-1):
        option.append([ maximum(x) for x in zip(option[-1][:-1],option[-1][1:],asset(n))])

        # sort option list in ascending time
    option.reverse()
    
        # return option price  tree
    return option'''