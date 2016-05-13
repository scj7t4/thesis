import numpy as np
import sys

p = 0.75
exp = 8
procs = 3

d = dict([ (i,0) for i in range(procs+1)])
for x in range(100000):
    g = [ np.random.binomial(1, p**exp) for i in range(procs) ]
    d[sum(g)] += 1
    
print d