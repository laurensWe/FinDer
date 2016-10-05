import numpy as np
S1 = 2 # 332712 - Max Dubber
S2 = 5 # 366515 - Laurens Weijs
S3 = 5 # 384825 - Jinchen Li
S4 = 9 # 388049 - Sebastiaan Vermeulen
S0 = K = round(5*(S2+S3)/2)
c = S1/100
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
                 
    def toString(self):
        out = ''
        for i in range(self.N,-self.N-1,-1):
            out += '\r\n----'+ '-'*(self.N+1)*12 
            for p in ['S','f','x','y']:
                out += '\r\n{: 2d}: '.format(i)
                for t in self.tree:
                    if i in self.tree[t]:
                        out += ' '*3 + '{}{:8.2f}'.format(p,self.tree[t][i][p])
                    else:
                        out += ' '*12
        return out
    
    def price(self):
        return round(self.tree[0][0]['f'],2)
    
if __name__=='__main__':
    op = OptionPricer(S=S0,K=K,sigma=sigma,c=c,N=2,ls='short')
    s=op.toString()#(S0, K, sigma, c=c, N=1)
    option_price = op.price()
    n=1
    Along = OptionPricer(10,10,.2,.1,n,'long').price()
    Ashort= OptionPricer(10,10,.2,.1,n,'short').price()
    
    s=OptionPricer(10,10,.2,.1,n,'short').toString()    
    
    from matplotlib import pyplot as plt
    x = np.arange(1,5)
    y = [OptionPricer(10,10,.2,.1,n,'short').price() for n in x]
    z = [OptionPricer(10,10,.2,.1,n,'long').price() for n in x]
    plt.xkcd()
    plt.plot(x,y,c='r')
    plt.plot(x,z,c='k')
    plt.xlabel('no. of ticks per time unit')
    plt.ylabel('bid-ask spread')
    plt.title('long vs short on Euro call options')
     