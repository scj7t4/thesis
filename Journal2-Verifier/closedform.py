from scipy.misc import comb
import itertools
from multiprocessing import Pool
import sys
import json

MULTI_P = 0
MULTI_N = 0

def probayc(p,m,k):
    if 0 <= k <= m:
        return comb(m,k)*(p**(2*k))*(1-p**2)**(m-k)
    else:
        return 0

def probelect(p,n,k):
    if 0 <= k <= n:
        return comb(n,k)*(p**(8*k))*(1-p**8)**(n-k)
    else:
        return 0

def probtrans(p,s,sp,n):
    #v = 0.0
    # s is the number of members in the current group +1
    # sp is the number of members in the new group (+1)
    return sum(map(lambda i: probayc(p,s-1,i)*probelect(p,n-s,sp-i-1),range(s)))
    """
    for i in range(s):
        # i out of s members stay in the group
        j = sp-i-1
        # j members join the group.
        # Probability that out of s-1 members i stay in
        # Probability that out of n-s processes j join
        v += probayc(p,s-1,i)*probelect(p,n-s,j)
    return v
    """

def multiprob(x):
    i,j = x
    return ("({},{})".format(i,j), probtrans(MULTI_P,i,j,MULTI_N))
    
def matrix(p,n):
    global MULTI_P, MULTI_N
    MULTI_N = n
    MULTI_P = p

    indexes = itertools.product(range(1,n+1), repeat=2)
    i1, i2 = itertools.tee(indexes)
    
    p = Pool(5)
    c = {}
    r = p.map(multiprob, i1, chunksize=1024)
    
    c = dict(r)
    return c

if __name__ == "__main__":
    r = {}
    for p in range(5,100,5):
        p = p/100.0
        r[p] = matrix(p,int(sys.argv[1]))
    with open('{}.dat'.format(sys.argv[1]), 'w+') as fp:
        json.dump(r,fp, indent=2)