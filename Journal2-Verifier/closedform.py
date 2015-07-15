import scipy.misc.comb as comb

def probayc(p,k,m):
    if 0 <= k <= m:
        return comb(m,k)*(p**(2*k))*(1-p**2)**(m-k)
    else:
        return 0.0

def probelect(p,k,n):
    if 0 <= k <= n:
        return comb(n,k)*(p**(8*k))*(1-p**8)**(n-k)
    else:
        return 0.0

def probtrans(s,sp,n,p):
    v = 0.0
    for i in range(s):
        for j in range(sp-i):
            v += probayc(p, i,s-1)*probelect(p, j,n-s-1)
    return v
    
def matrix(p,n):
    c = {}
    for i in range(n)
