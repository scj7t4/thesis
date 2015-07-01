import chain
import gm
import itertools

PROCS = 3
P = 0.65

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
    print "TOTALS: {}".format(tots)
    print "DESIGN: {}".format(design)
    print "CHAIN: {}".format(chain)
    for k in s:
        dv = tots[k[0]] * design[k] if k in design else 0.0
        cv = chain[k] if k in chain else 0.0
        if dv != 0:
            error[k] = (dv-cv)**2 / dv
        else:
            print "ERROR {}".format(k)
            assert cv == 0.0
    return error

def sumdict(d):
    s = 0
    for k in d:
        s += d[k]
    return s
    
if __name__ == "__main__":
    #CHAIN 2 c = {(1, 2): 0.07432864802842075, (1, 1): 0.9256713519715792, (2, 1): 0.7196880675141545, (2, 2): 0.2803119324858455}
    #CHAIN 4 c = {(1, 2): 0.18765339878348095, (3, 2): 0.4659239842726081, (1, 3): 0.015953473482018993, (3, 3): 0.06094364351245085, (4, 1): 0.2391304347826087, (3, 1): 0.47182175622542594, (4, 4): 0.043478260869565216, (2, 1): 0.6210835926510081, (1, 1): 0.7958862447977804, (2, 3): 0.009633829233982693, (1, 4): 0.0005068829367196671, (4, 3): 0.2391304347826087, (2, 2): 0.36911206786308026, (4, 2): 0.4782608695652174, (3, 4): 0.001310615989515072, (2, 4): 0.00017051025192889722}
    #CHAIN 3 c = {(1, 2): 0.1340519959256924, (3, 2): 0.4292763157894737, (1, 3): 0.00630547606344279, (3, 3): 0.07730263157894737, (3, 1): 0.4934210526315789, (2, 1): 0.6662530284228565, (2, 3): 0.0024227382851740235, (2, 2): 0.3313242332919695, (1, 1): 0.8596425280108648}
    #CHAIN 5 c = {(1, 2): 0.22940900011749502, (3, 2): 0.5040083652840711, (1, 3): 0.029491246622018564, (3, 3): 0.06936214708957825, (3, 4): 0.0003485535029627048, (4, 2): 0.43478260869565216, (3, 1): 0.42628093412338797, (4, 4): 0.018633540372670808, (2, 1): 0.5710624740268735, (1, 1): 0.7390289037715897, (1, 5): 7.343437903889085e-05, (4, 1): 0.3416149068322981, (2, 3): 0.02171353373043358, (1, 4): 0.001997415109857831, (4, 3): 0.20496894409937888, (2, 2): 0.4064967447014822, (5, 1): 0.4, (5, 2): 0.2, (2, 4): 0.000727247541210694, (5, 3): 0.4}
    c = gm.make_chain(PROCS,P)
    minv = (10000000,None,None)
    for m in range(1,2):
        for spvs in itertools.product(range(30,31), repeat=PROCS-1):
            sp = {1:4.0}
            for index, v in enumerate(spvs):
                v /= 10.0
                sp[index+2] = v
            chain.setvals(sp,m)
            try:
                d = chain.design(PROCS,P)
                print d
                e = sumdict(error(d,c))
            except AssertionError:
                print "Can't make design {} m:{}".format(sp, m)
                continue
            print "sp {} m {} error {}".format(sp,m,e)
            minv = min(minv, (e,sp,m))
    
    print minv 
