import cfnumpy
import gm
import math
import pykov

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

if __name__ == "__main__":
    r = {}
    #CHAIN 2 c = {(1, 2): 0.07432864802842075, (1, 1): 0.9256713519715792, (2, 1): 0.7196880675141545, (2, 2): 0.2803119324858455}
    #CHAIN 4 c = {(1, 2): 0.18765339878348095, (3, 2): 0.4659239842726081, (1, 3): 0.015953473482018993, (3, 3): 0.06094364351245085, (4, 1): 0.2391304347826087, (3, 1): 0.47182175622542594, (4, 4): 0.043478260869565216, (2, 1): 0.6210835926510081, (1, 1): 0.7958862447977804, (2, 3): 0.009633829233982693, (1, 4): 0.0005068829367196671, (4, 3): 0.2391304347826087, (2, 2): 0.36911206786308026, (4, 2): 0.4782608695652174, (3, 4): 0.001310615989515072, (2, 4): 0.00017051025192889722}
    #CHAIN 3c = {(1, 2): 0.1340519959256924, (3, 2): 0.4292763157894737, (1, 3): 0.00630547606344279, (3, 3): 0.07730263157894737, (3, 1): 0.4934210526315789, (2, 1): 0.6662530284228565, (2, 3): 0.0024227382851740235, (2, 2): 0.3313242332919695, (1, 1): 0.8596425280108648}
    #CHAIN 5 c = {(1, 2): 0.22940900011749502, (3, 2): 0.5040083652840711, (1, 3): 0.029491246622018564, (3, 3): 0.06936214708957825, (3, 4): 0.0003485535029627048, (4, 2): 0.43478260869565216, (3, 1): 0.42628093412338797, (4, 4): 0.018633540372670808, (2, 1): 0.5710624740268735, (1, 1): 0.7390289037715897, (1, 5): 7.343437903889085e-05, (4, 1): 0.3416149068322981, (2, 3): 0.02171353373043358, (1, 4): 0.001997415109857831, (4, 3): 0.20496894409937888, (2, 2): 0.4064967447014822, (5, 1): 0.4, (5, 2): 0.2, (2, 4): 0.000727247541210694, (5, 3): 0.4}
    for p in range(55,100,5):
        p /= 100.0
        c, c2 = gm.make_chain(4,p,iters=100)
        print "PROB {}".format(p)
        print "CHAIN\n{}".format(dictpp(gm.chainify(c)))
        #chain.setvals({1:3.0, 2: 3.0, 3: 3.0, 4: 3.0, 5:3.0, 6:3.0})
        d = cfnumpy.design(4,p)
        print "DESIGN\n{}".format(dictpp(d))
        e = error(d,c)
        print "ERROR\n{}".format(dictpp(e))
        r[p] = (sumdict(e), descrim(d,c))
        
    for p in r:
        print "{}\t{}".format(p, tuptocols(r[p]))
