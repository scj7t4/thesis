from numpy.random import binomial

def trial(p0,p1):
    c = 1
    cont = binomial(1,p0)
    while cont:
        c += 1
        cont = binomial(1,p1)
    return c

TRIALS = 10000

for i in range(5,100,5):
    p = i/100.0
    p0, p1 = p**3, p**4
    c = 0
    for i in range(TRIALS):
        c += trial(p0,p1)
    avg = c / float(TRIALS)
    px = 1 - (1 / avg)
    print "{} : {} ({}x{} -> {})".format(p,avg,p0,p1,px)
