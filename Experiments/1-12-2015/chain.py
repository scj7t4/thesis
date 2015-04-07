import pykov

def AYCsFail(p):
    return 2*(p**2)*(1-p**2)+(1-p**2)**2;

def make_chain(p):
    chain = {
        # Checked
        ('1,1','1,1') : AYCsFail(p)+((p**2)**2)*(1-p**2),
        # !(AYC^AYC^INV^ACCEPT)
        ('1,1','1,2') : 0,               # Not possible
        ('1,1','2,1') : (p ** 6)*(1-p),  # AYC^AYC^INV^ACCEPT^!PEERLIST
        ('1,1','2,2') : (p ** 7),        # AYC^AYC^INV^ACCEPT^PEERLIST
        # Checked
        ('1,2','1,1') : 1,               # Member does not detect failure until it can't elect
        ('1,2','1,2') : 0,               # Not possible
        ('1,2','2,1') : 0,               # Not possible
        ('1,2','2,2') : 0,               # Not possible
        # Checked
        ('2,1','1,1') : AYCsFail(p)+((p**2)**2)*(1-p**2),
        # AYC^AYC^!(INV^ACCEPT) | !(AYC) | !(AYC) | !(AYC*AYC)
        ('2,1','1,2') : 0,               # Not Possible
        ('2,1','2,1') : (p ** 6)*(1-p),  # AYC^AYC^INV^ACCEPT^!PEERLIST
        ('2,1','2,2') : (p ** 7),        # AYC^AYC^INV^ACCEPT^PEERLIST
        # Checked
        ('2,2','1,1') : (1-p**2)**2,     # !AYC ^ !AYC
        ('2,2','1,2') : (p**2)*(1-p**2), # AYC ^ !AYC
        ('2,2','2,1') : (p**2)*(1-p**2), # AYC ^ !AYC
        ('2,2','2,2') : (p**2)**2,       # AYC ^ AYC  
    }
    return chain

def chain_state_to_proj_state(fs):
    (fr,_) = fs.split(',')
    return fr
 
def chain_key_to_proj_key(fs,ts):
    fr = chain_state_to_proj_state(fs)
    to = chain_state_to_proj_state(ts)
    return (fr,to)
    
def project_transitions(p):
    chain = make_chain(p)
    #A projection is created by finding the steady state of the whole chain:
    T = pykov.Chain(chain)
    ss = T.steady()
    print ss
    # We then need to transform the steady state into the probability you're in
    # state x v y
    normalsteady = {}
    for fs in ss:
        proj = chain_state_to_proj_state(fs)
        try:
            normalsteady[proj].append( (fs,ss[fs]) )
        except KeyError:
            normalsteady[proj] = [ (fs,ss[fs]) ]
    
    # Produce the probability which original state you are in given you in the projected
    # state x.
    normalsteady2 = {}
    for key in normalsteady:
        normalsteady2[key] = {}
        s = sum([ x[1] for x in normalsteady[key] ])
        assert s <= 1
        for i in range(len(normalsteady[key])):
            k = normalsteady[key][i][0]
            normalsteady2[key][k] = normalsteady[key][i][1]/s
    
    #print "NORAML STEADY ",normalsteady2
    
    #normalsteady2 now has the probability of being in a fully described state. You can
    #use that to estimate the projection
    collapsed = {}
    for (fs,ts) in chain:
        fr,to = chain_key_to_proj_key(fs,ts)
        try:
            collapsed[ (fr,to) ].append( (fs,ts) )
        except KeyError:
            collapsed[ (fr,to) ] = [ (fs,ts) ]
    
    newchain = {}
    # Collapsed is the projection transition, and the actual transitions that can happen
    #print "COLLAPSED ",collapsed
    
    for key in collapsed:
        newchain[ key ] = 0
        for oldstate in collapsed[key]:
            oc = chain[oldstate]
            nc = normalsteady2[key[0]][oldstate[0]]
            newchain[ key ] +=  nc * oc
    return newchain
    
if __name__ == "__main__":
    c2 = project_transitions(.95)
    T = pykov.Chain(c2)
    print T.steady()
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        