import numpy as np

INPUT_LEN = 100
XSCALE = 0.001

def EWMA(alpha, s, seq):
    n = len(seq)
    v = s * (1-alpha) ** n
    vs = [v]
    for (i, xi) in enumerate(seq, start=1):
        t = xi*(alpha)*(1-alpha)**(n-i)
        vs.append(t)
    return sum(vs)

def EWMA2(alpha, sy, sx, a, d, seqx):
    n = len(seqx)
    v = [(sy-a*sx) * (1 - alpha)**(n)]
    v.append( a * EWMA(alpha, sx, seqx) )
    v.append(sum([ d * alpha * (1-alpha) ** (n-i) for (i,_) in enumerate(seqx, start=1) ]))
    v.sort()
    print v
    return sum(v)

def DIFF(alpha, sy, sx, a, d, seqx):
    n = len(seqx)
    t1 = (sy-sx)*(1-alpha)**n
    t2 = sum([ alpha * (a - 1) * xi * (1-alpha) ** (n-i) for (i, xi) in enumerate(seqx, start=1) ])
    t3 = sum([ alpha * d * (1-alpha) ** (n-i) for (i,_) in enumerate(seqx, start=1)] )
    return t1+t2+t3

para_m = -713.0
para_b = 450

para_n = -713.0+244.0
para_e = 450

para_a = para_n / para_m
para_d = (para_e - para_b*para_a)

print "{m}x+{b} => {n}x+{e} via {a}({m}x+{b})+{d}".format(m=para_m, b=para_b, n=para_n, e=para_e, a=para_a, d=para_d)

test_seq = [ para_m*(x*XSCALE) + para_b for x in range(INPUT_LEN) ]
test_seq2 = [ para_n*(x*XSCALE) + para_e for x in range(INPUT_LEN) ]
test_s = 60
test_s2 = 60
test_alpha = 0.002

for x in range(INPUT_LEN):
    inp = test_seq[:x]
    inp2 = test_seq2[:x]
    to_print = [
        x*XSCALE,
        test_seq[x], 
        EWMA(test_alpha, test_s, inp),
        test_seq2[x],
        EWMA(test_alpha, test_s2, inp2),
        EWMA2(test_alpha, test_s2, test_s, para_a, para_d, inp),
        DIFF(test_alpha, test_s2, test_s, para_a, para_d, inp),
    ]
    fstring = "\t".join([ "{}" ] * len(to_print))
    print fstring.format(*to_print)
