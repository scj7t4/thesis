import chain
import pykov

PROCS = 100

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
    
for p in range(5,100,5):
    p /= 100.0
    d = chain.design(PROCS, p)
    d[(1,1)] -= 0.000000001
    #inspect(d)
    T = pykov.Chain(d)
    ss = T.steady()
    v = [ str(ss[s]) for s in ss ]
    print "{}\t{}".format(p,"\t".join(v))
    
  
