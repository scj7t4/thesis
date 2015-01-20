import pykov


def make_chain(p):
    si = p ** 6
    ig = p ** 3
    gg = p ** 4
    chain_dict = {
        ('Solo','Interim') : si,
        ('Solo','Solo')    : 1-si,
        ('Interim','Group'): ig, 
        ('Interim','Solo') : 1-ig,
        ('Group','Group')  : gg,
        ('Group','Solo')   : 1-gg,
    }
    return chain_dict

for i in range(0,105,5):
    p = i / 100.0
    T = pykov.Chain(make_chain(p))
    ss = T.steady()
    g = ss['Interim'] + ss['Group']
    print "{}\t{}\t{}".format(p,ss['Solo'],g)

