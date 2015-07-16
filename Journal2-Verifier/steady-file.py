import chain
import pykov
import json
import sys
import itertools

def inspect(d):
    # This is the amount that I actually care about for error
    EPSILON = 0.0001
    vd = {}
    adjkey = {}
    # Figure out how close each row is to 1
    for (f,t) in d:
        try:
            vd[f] += d[(f,t)]
        except KeyError:
            vd[f] = d[(f,t)]
        adjkey[f] = t
    
    print vd
    """
    # for each row
    for s in vd:
        diff = 1.0-vd[s]
        # Confirm that the error from the model is less than EPSILON
        #print diff
        assert(abs(diff) < EPSILON)
        # Anything less is residue from float multiplies and we'll just
        # correct for them the to get rid of them.
        if diff > 0.0:
            d[(s,s)] -= diff
        if diff < 0.0:
            d[(s,s)] += diff
    return d
    """

def entuple(d):
    o = {}
    for k in d:
        o[eval(k)] = d[k]
    return o
    
def dictify(l2d):
    d = {}
    s = len(l2d)
    lg = itertools.chain(*l2d)
    indexes = itertools.product(range(1,s+1), repeat=2)
    return dict(itertools.izip(indexes, lg))
    
def everything(d):
    maxk = max(d.iterkeys())
    l = [ 0 for _ in range(maxk) ]
    for k in d:
        l[k-1] = d[k]
    return l
    
c = {}
with open(sys.argv[1]) as fp:
    c = json.load(fp)
    
for p in c:
    #print p
    d = dictify(c[p])
    #print d
    #print inspect(d)
    d[(1,1)] -= 0.000000000001
    T = pykov.Chain(d)
    ss = T.steady()
    v = [ str(x) for x in everything(ss) ]
    print "{}\t{}".format(p,"\t".join(v))
    
  
