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
        
    def replicatingPortfolio(self,c,ls): 
        def xyf(t,s,su,yu,xu,sd,yd,xd): 
            cu,cd = (1+c,1-c) if ls=='long' or t+1<self.N else (1-c,1+c)
            y = (xu-xd+yu*su*cu-yd*sd*cd)/(su*cu-sd*cd)
            x =  xd+(yd-y)*sd*cd 
            f = x + y*s
            return {'x':x,'y':y,'f':f}
        return xyf 
        
    def setFinalPrice(self,K,tree,N,ls):
        for i in tree[N]:
            S = tree[N][i]['S']
            S_= tree[N-1][i+1 if i<N else i-1]['S']
            if ls=='long':
                tree[N][i].update({'f':max(0,S-K),'x':-float(S>K)*S_,'y':float(S>K)})
            else:
                tree[N][i].update({'f':-max(0,S-K),'x':float(S>K)*S_,'y':-float(S>K)})
     
    def initTree(self,S,sigma,N):
        price = lambda u,d: S*np.exp(sigma*np.sqrt(u/N)-sigma*np.sqrt(d/N))
        return {t:{t-2*i:{'S':price(t-i,i)} for i in range(t+1)} for t in range(N+1)}
      
    def fillTree(self,S,K,sigma,c,N,ls,tree):
        # recur through the option tree
        recur = self.replicatingPortfolio(c,ls)
        for t in range(N-1,-1,-1):
            for i in tree[t]:
                tree[t][i].update(recur(t,tree[t][i]['S'],  #S
                                     tree[t+1][i+1]['S'], #Su
                                     tree[t+1][i+1]['y'], #yu
                                     tree[t+1][i+1]['x'], #xu
                                     tree[t+1][i-1]['S'], #Sd
                                     tree[t+1][i-1]['y'], #yd
                                     tree[t+1][i-1]['x']))#xd
        return tree
                 
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
    op = OptionPricer(S=S0,K=K,sigma=sigma,c=c,N=10,ls='short')
    s=op.toString()#(S0, K, sigma, c=c, N=1)
    option_price = op.price()
    n=1
    Along = OptionPricer(10,10,.2,.1,n,'long').price()
    Ashort= OptionPricer(10,10,.2,.1,n,'short').price()
    
     