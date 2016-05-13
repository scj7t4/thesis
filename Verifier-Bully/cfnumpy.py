from scipy.misc import comb
import itertools
from multiprocessing import Pool
import sys
import json
import collections
import functools
import numpy as np

MULTI_P = 0
MULTI_N = 0

class memoized(object):
   '''Decorator. Caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned
   (not reevaluated).
   '''
   def __init__(self, func):
      self.func = func
      self.cache = {}
   def __call__(self, *args):
      if not isinstance(args, collections.Hashable):
         # uncacheable. a list, for instance.
         # better to not cache than blow up.
         return self.func(*args)
      if args in self.cache:
         return self.cache[args]
      else:
         value = self.func(*args)
         self.cache[args] = value
         return value
   def __repr__(self):
      '''Return the function's docstring.'''
      return self.func.__doc__
   def __get__(self, obj, objtype):
      '''Support instance methods.'''
      return functools.partial(self.__call__, obj)

@memoized
def combtable(dim):
    cols = itertools.chain(*itertools.repeat(xrange(dim),dim))
    rows = itertools.chain(*itertools.imap(lambda x: itertools.repeat(x,dim), range(dim)))
    ns = np.fromiter(rows, np.dtype('d'))
    ks = np.fromiter(cols, np.dtype('d'))
    o = comb(ns,ks)
    return np.reshape(o,(dim,dim))

def np_prob(dim,p,power):
    a = np.full(dim, p**power)
    b = np.full((dim,dim), (1-p**power))
    r = np.fromiter(xrange(dim), np.dtype('d'))
    a = np.power(a, r)
    bp = np.reshape(r, (dim,1))-r
    bp = bp.clip(0)
    b = np.power(b, bp)
    s1 = b*a
    return s1*combtable(dim)

@memoized
def np_probayc(dim,p):
    return np_prob(dim,p,4)

@memoized
def np_probelect(dim,p):
    return np_prob(dim,p,8)

def np_probtrans(p, s, sp, n):
    ayc = np_probayc(n,p)
    elect = np_probelect(n,p)
    ayc_slice = ayc[s-1,:]
    slicelen = s #(sp-1)-(sp-s)
    #This needs to get sliced to select parts of it. and then padded.
    elect_slice = elect[n-s,:]
    elect_slice = elect_slice[max(0,sp-s):sp]
    les = elect_slice.shape[0]
    elect_slice = np.pad(elect_slice,(n-les,0),'constant')[::-1] # defaults to 0
    return np.sum(ayc_slice*elect_slice)

@memoized
def probayc(p,m,k):
    if 0 <= k <= m:
        return comb(m,k)*(p**(2*k))*(1-p**2)**(m-k)
    else:
        return 0

@memoized
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

def VERIFY(n):
    c = 0
    for PROB in [0.75,0.5,0.95,0.1]:
        for s in range(1,n+1):
            for sp in range(1,n+1):
                c+=1
                r1 = probtrans(PROB, s, sp, n)
                r2 = np_probtrans(PROB, s, sp, n)
                delta = abs(r1-r2)
                if abs(r1-r2) > 0.00000001:
                    print "BAD RESULT {}->{} n={} delta={}".format(s,sp,n,delta)
    print "Verified {} designs".format(c)
    
def multiprob(x):
    i,j = x
    return ("({},{})".format(i,j), probtrans(MULTI_P,i,j,MULTI_N))
    
def matrix(p,n):
    global MULTI_P, MULTI_N
    MULTI_N = n
    MULTI_P = p

    indexes = itertools.product(range(1,n+1), repeat=2)
    i1, i2 = itertools.tee(indexes)
    
    #p = Pool(5)
    c = {}
    r = map(multiprob, i1)
    
    c = dict(r)
    return c
    
def np_matrix(p,n):
    vfunc = np.vectorize(np_probtrans,excluded=(0,3),otypes=(np.dtype('d'),))
    return np.fromfunction(lambda s,sp: vfunc(p,s+1, sp+1, n),(n,n))

def np_matrix_star(t):
    return np_matrix(t[0], t[1])

def design(n,p):
    mtx = np_matrix(p,n)
    d = {}
    for i in range(n):
        for j in range(n):
          d[(i+1,j+1)] = mtx[i,j]
    return d  
    
if __name__ == "__main__":
    r = {}
    p = range(5,100,5)
    p = map(lambda x: x/100.0, p)
    args = zip(p,itertools.repeat(int(sys.argv[1])))
    workers = Pool()
    r = workers.map(np_matrix_star, args)
    r = zip(p, map(lambda x: x.tolist(), r))
    o = dict(r)
    with open('{}.dat'.format(sys.argv[1]), 'w+') as fp:
        json.dump(o,fp, indent=2)
