from gm import *
import pickle

observations = []
syst = []

for i in range(100):
    with open('scenario.pickle') as cfp:
        syst = pickle.load(cfp)
    ob = len(syst[0].group)+1    
    observations.append(ob)
    logging.info(str(syst))
    applyonce(syst)
    ob = len(syst[0].group)+1
    observations.append( ob )
    logging.info(str(syst))
    observations.append('X')    

o = observe(observations)
pretty(o)
c = chainify(o)
pretty(c)
#return (o, likely_observe(observations))