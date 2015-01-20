#Verify that my prediction conforms to the events that should be occuring

import numpy

def ayc(p):
    return True if numpy.random.binomial(1,p) and numpy.random.binomial(1,p) else False

def ayc_alt(p):
    return True if numpy.random.binomial(2,p) == 2 else False

def invite(p):
    return True if numpy.random.binomial(1,p) else False

def accept(p):
    return True if numpy.random.binomial(1,p) else False

TRIALS = 100000
chi2 = 0
chi3 = 0
chiold = 0
print "p\tt1\tt2\tt3\tt4\tt5"
for p in range(0,105,5):
    p /= 100.0
    s = 0
    s2 = 0
    s3 = 0
    for _ in range(TRIALS):
        if ayc(p) and ayc(p) and invite(p) and accept(p):
            s += 1.0
        if ayc_alt(p) and ayc_alt(p) and invite(p) and accept(p):
            s2 += 1.0
        if numpy.random.binomial(6,p) == 6:
            s3 += 1.0
    s /= TRIALS
    s2 /= TRIALS
    s3 /= TRIALS
    if s > 0:
        chi2 += (s2-s)**2 / s
        chi3 += (s3-s)**2 / s
        chiold += (p**6 - s) ** 2 / s
    print "{}\t{}\t{}\t{}".format(p, s, s2, s3)
print "Chi2 {}".format(chi2)
print "Chi3 {}".format(chi3)
print "Chiold {}".format(chiold)
