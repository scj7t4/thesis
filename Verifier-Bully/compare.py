import gm
import math
import pykov
import markov

EF = 100

def error(design, chain):
    tots = {}
    error = {}
    s = set([k for k in design])
    for k in chain:
        s.add(k)
    for k in s:
        tots[k[0]] = 0
    for k in chain:
        tots[k[0]] += chain[k]
    print chain
    print tots
    for k in s:
        #dv = tots[k[0]] * design[k] if k in design else 0.0
        #cv = chain[k] if k in chain else 0.0
        ni = tots[k[0]]
        phat = chain[k] / float(ni) if k in chain else 0.0
        p0 = float(design[k]) if k in design else 0.0
        print "K {} : ni={} phat={} p0={}".format(k, ni, phat, p0)
        if p0 > 0:
            error[k] = (ni*(phat-p0)**2) / p0
        else:
            assert phat == 0.0
    return error

def descrim(design, chain):
    T = pykov.Chain(design)
    pi = T.steady()
    mmax = 0
    tots = {}
    for (i,j) in chain:
        mmax = max(i,j,mmax)
    for k in chain:
        try:
            tots[k[0]] += chain[k]
        except KeyError:
            tots[k[0]] = chain[k]
    s = 0.0
    for i in range(mmax):
        for j in range(mmax):
            if (i,j) not in chain:
                continue
            pij = design[(i,j)]
            tij = chain[(i,j)] / float(tots[i])
            s += pi[i] * pij * math.log(pij/float(tij))
    return s
    
def loglikely(design, chain):
    mmax = 0
    ni = {}
    for (i,j) in chain:
        mmax = max(i,j,mmax)
        try:
            ni[i] += chain[(i,j)]
        except KeyError:
            ni[i] = chain[(i,j)]
    s = 0.0
    for i in range(mmax):
        for j in range(mmax):
            if (i,j) not in chain:
                continue
            numer = chain[(i,j)]
            denom = ni[i] * design[(i,j)]
            s += chain[(i,j)] * math.log(numer/float(denom))
    s *= 2
    return s

def tloglikely(design, chain):
    tmax = 0
    mmax = 0
    nti = {}
    for (t,i,j) in chain:
        tmax = max(t,tmax)
        mmax = max(i,j,mmax)
        try:
            nti[(t,i)] += chain[(t,i,j)]
        except KeyError:
            nti[(t,i)] = chain[(t,i,j)]
    s = 0.0
    for t in range(tmax):
        for i in range(mmax):
            for j in range(mmax):
                if (t,i,j) not in chain:
                    continue
                numer = chain[(t,i,j)]
                denom = (nti[(t,i)]*design[(i,j)])
                s += chain[(t,i,j)] * math.log(numer/float(denom))
    s *= 2
    return s

def sumdict(d):
    s = 0
    for k in d:
        s += d[k]
    return s

def dictpp(d):
    s = ""
    for k in d:
         s += "{}: {}\n".format(k, d[k])
    return s

def tuptocols(tup,joiner='\t'):
    l = [ str(x) for x in tup ]
    return joiner.join(l)

PROCS = 5
PERSPECTIVE = 1

if __name__ == "__main__":
    r = {}
    for p in range(55,100,5):
        p /= 100.0
        c, c2 = gm.make_chain(PROCS,p,iters=500,perspective=PERSPECTIVE)
        print "PROB {}".format(p)
        print "CHAIN\n{}".format(dictpp(gm.chainify(c)))
        #chain.setvals({1:3.0, 2: 3.0, 3: 3.0, 4: 3.0, 5:3.0, 6:3.0})
        d = markov.design(p, PROCS, PERSPECTIVE)
        print "DESIGN\n{}".format(dictpp(d))
        e = error(d,c)
        print "ERROR\n{}".format(dictpp(e))
        r[p] = (sumdict(e), 0.0)
        
    for p in r:
        print "{}\t{}".format(p, tuptocols(r[p]))
