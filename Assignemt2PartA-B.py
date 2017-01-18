import numpy as np
S1 = 2 # 332712 - Max Dubber
S2 = 5 # 366515 - Laurens Weijs
S3 = 5 # 384825 - Jinchen Li
S4 = 9 # 388049 - Sebastiaan Vermeulen
S0 = K = round(5*(S2+S3)/2)
C = S1/100
sigma = max(0.15, S4/20)

class OptionPricer(object):
    def __init__(self,S,K,sigma,c=0,N=1,ls='long'):
        self.N = N
        self.tree = self.initTree(S,sigma,N)
        self.setFinalPrice(K,self.tree,N,ls)
        self.fillTree(S,K,sigma,c,N,ls,self.tree)
        
    def setFinalPrice(self,K,tree,N,ls):
        for i in tree[N]:
            S = tree[N][i]['S']
            if ls=='long':
                tree[N][i].update({'f':max(0,S-K),'x':-float(S>K)*K,'y':float(S>K)})
            else:
                tree[N][i].update({'f':-max(0,S-K),'x':float(S>K)*K,'y':-float(S>K)})
     
    def initTree(self,S,sigma,N):
        price = lambda u,d: S*np.exp(sigma*np.sqrt(u/N)-sigma*np.sqrt(d/N))
        return {t:{t-2*i:{'S':price(t-i,i)} for i in range(t+1)} for t in range(N+1)}
      
    def fillTree(self,S,K,sigma,c,N,ls,tree):
        for t in range(N-1,-1,-1):
            for i in tree[t]:
                self.recur(c,ls,{'0':tree[t][i],'u':tree[t+1][i+1],'d':tree[t+1][i-1]})

    def recur(self,c,ls,t):
        cu,cd = (1+c,1-c) if ls=='long' else (1-c,1+c)
        t['0']['y'] = (t['u']['x']-t['d']['x']+t['u']['y']*t['u']['S']*cu-t['d']['y']*t['d']['S']*cd)/(t['u']['S']*cu-t['d']['S']*cd)
        t['0']['x'] =  t['d']['x']+(t['d']['y']-t['0']['y'])*t['d']['S']*cd 
        t['0']['f'] = t['0']['x'] + t['0']['y']*t['0']['S']
    
    def price(self):
        return abs(round(self.tree[0][0]['f'],2))
                 
    def toString(self):
        out = ''
        for i in range(self.N,-self.N-1,-1):
            out += '\r\n----'+ '-'*(self.N+1)*12 
            for p in ['S','f','x','y']:
                out += '\r\n{: 2d}: '.format(i)
                for t in self.tree:
                    if i in self.tree[t]:
                        out += ' '*3 + '{}{:8.2g}'.format(p,self.tree[t][i][p])
                    else:
                        out += ' '*12
        return out
    
if __name__=='__main__':
    np.seterr(invalid='raise')
    op = OptionPricer(S=S0,K=K,sigma=sigma,c=C,N=1,ls='long').price()
    
    x = np.arange(1,100)    
    y = [OptionPricer(S=S0,K=K,sigma=sigma,c=C,N=n,ls='long').price() for n in x]
    z = [OptionPricer(S=S0,K=K,sigma=sigma,c=0,N=n,ls='long').price() for n in x]
    
    from matplotlib import pyplot as plt,style
    style.use('seaborn-whitegrid')
    plt.close('all')
    
    x = np.arange(.01,1,.05)
    y = [OptionPricer(S=S0,K=K,sigma=s,c=C,N=50,ls='long').price() for s in x]
    plt.plot(x,y)
    plt.xlabel('volatility')
    plt.ylabel('Option price')
    
    x = np.arange(.01,.20,.01)
    y = [OptionPricer(S=S0,K=K,sigma=sigma,c=c,N=50,ls='long').price() for c in x]
    plt.plot(x,y)
    plt.xlabel('transaction cost')
    plt.ylabel('Option price')
    
    
    if False:
        s=sigma;c=C;k=K;
        y = [OptionPricer(S=S0,K=K,sigma=s,c=c,N=n,ls='long').price() for n in x]
        plt.plot(x,y,linewidth=5,label='c: {:2.0%} $\sigma$: {:.2f} K:{:d}'.format(c,s,k))
        
        s=sigma;c=0;k=K;
        y = [OptionPricer(S=S0,K=K,sigma=s,c=c,N=n,ls='long').price() for n in x]
        plt.plot(x,y,label='c: {:2.0%} $\sigma$: {:.2f} K:{:d}'.format(c,s,k))
        
        s=sigma*2;c=C;k=K;
        y = [OptionPricer(S=S0,K=K,sigma=s,c=c,N=n,ls='long').price() for n in x]
        plt.plot(x,y,label='c: {:2.0%} $\sigma$: {:.2f} K:{:d}'.format(c,s,k))
        
        s=sigma*2;c=0;k=K;
        y = [OptionPricer(S=S0,K=K,sigma=s,c=c,N=n,ls='long').price() for n in x]
        plt.plot(x,y,label='c: {:2.0%} $\sigma$: {:.2f} K:{:d}'.format(c,s,k))
        
        s=sigma;c=C;k=K+5
        y = [OptionPricer(S=S0,K=k,sigma=s,c=c,N=n,ls='long').price() for n in x]
        plt.plot(x,y,label='c: {:2.0%} $\sigma$: {:.2f} K:{:d}'.format(c,s,k))
        
        s=sigma;c=C;k=K-5
        y = [OptionPricer(S=S0,K=k,sigma=s,c=c,N=n,ls='long').price() for n in x]
        plt.plot(x,y,label='c: {:2.0%} $\sigma$: {:.2f} K:{:d}'.format(c,s,k))
        
        plt.xlabel('no. of ticks per time unit')
        plt.ylabel('price')
        plt.legend(title='parameters')
        #plt.savefig('C:/users/ms/desktop/{}.png')
         