import numpy as np
S1 = 2 # 332712 - Max Dubber
S2 = 5 # 366515 - Laurens Weijs
S3 = 5 # 384825 - Jinchen Li
S4 = 9 # 388049 - Sebastiaan Vermeulen
S0 = K = round(5*(S2+S3)/2)
c = S1/100
sigma = max(0.15, S4/20)

# assuming that executing an option means spending transaction cost twice
def recursivePrice(K,c,r,kind,pc):
    fun = lambda Pu,Pd,Su,Sd,S: (S-np.exp(-r)*Su)*(Pu-Pd)/(Su-Sd)+np.exp(-r)*Pu
    if kind=='E':
        return fun
    elif kind=='A' and pc=='put':
        return lambda Pu,Pd,Su,Sd,S: max(K-S-2*c,fun(Pu,Pd,Su,Sd,S))
    else:
        return lambda Pu,Pd,Su,Sd,S: max(S-K-2*c,fun(Pu,Pd,Su,Sd,S))
        
def finalPrice(K, c, pc, S):
    if pc=='put':
        return max(0,K-S-2*c)  
    else:
        return max(0,S-K-2*c)
 
def assetTree(S,mu,sigma,N):
    price = lambda u,d: S*np.exp(mu*(u+d)+sigma*np.sqrt(u)-sigma*np.sqrt(d))
    return [[price(t-i,i) for i in range(t+1)] for t in range(N+1)]
    
def deepMap(fun,vec):
    return [*map(lambda x: [*map(fun,x)],vec)]
    
def tree(S,K,sigma,c=0,mu=0,N=1,r=0,kind='E',pc='put'):
    # inits of asset and option trees
    asset = assetTree(S,mu,sigma/N,N)
    option = [[] for i in range(N+1)]
    # option trees final values
    option[-1].extend([finalPrice(K,c,pc,S) for S in asset[-1]])
    # recur through the option tree
    recur = recursivePrice(K,c,r,kind,pc)
    for i in range(N,0,-1):
        zipped = zip(option[i][:-1],option[i][1:],asset[i][:-1],asset[i][1:],asset[i-1])
        option[i-1].extend([recur(Pu,Pd,Su,Sd,S) for Pu,Pd,Su,Sd,S in zipped])
    # finalize and return
    return asset,option
    
def profit(option, ls='long'):
    if ls=='long':
        return [o - option[0][0] for o in option[-1]]
    else:
        return [option[0][0] - o for o in option[-1]]
        
def printTree(tree, profit = None):
    for line in tree:
        print('time {:3d}:'.format(len(line)-1)+'     '*(len(tree)-len(line)),end='')
        print(*map('{:9.2f}'.format, line))   
    if profit is not None:
        print('profit  :', end='')
        print(*map('{:9.2f}'.format, profit))
        
if __name__=='__main__':
    #TODO: sigma schalen met N
    asset, option = tree(S0, K, sigma, c=c, N=1, kind='E', pc='call')
    printTree(asset)
    print('\n\n')
    printTree(option,profit(option,'long'))
     