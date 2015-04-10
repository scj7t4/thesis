import pykov
import itertools
import functools
import collections
import functools

MIXINGVALUE = 3
SPVALUE = {}

def setvals(valued):
    global SPVALUE
    SPVALUE = valued

class memoized(object):
   '''Decorator. Caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned
   (not reevaluated).
   '''
   def __init__(self, func):
      self.func = func
      self.cache = {}
   def __call__(self, *args):
      if not isinstance(args, collections.Hashable):
         # uncacheable. a list, for instance.
         # better to not cache than blow up.
         return self.func(*args)
      if args in self.cache:
         return self.cache[args]
      else:
         value = self.func(*args)
         self.cache[args] = value
         return value
   def __repr__(self):
      '''Return the function's docstring.'''
      return self.func.__doc__
   def __get__(self, obj, objtype):
      '''Support instance methods.'''
      return functools.partial(self.__call__, obj)

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
    #power = 1/(p**3)
    power = MIXINGVALUE
    v = pykov.Vector()
    v[('1,1')] = 1.0
    ss = T.pow(v,int(power))
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
        for oldstate in collapsed[key]:
            try:
                oc = chain[oldstate]
                k1 = key[0]
                k2 = oldstate[0]
                nc = normalsteady2[k1][k2]
                f,t = key
                f = int(f)
                t = int(t)
            except KeyError:
                continue
            try:
                newchain[ (f,t) ] +=  nc * oc
            except KeyError:
                newchain[ (f,t) ] = nc*oc
    
    return newchain   

def sys_config(procs, p):
    assert(procs > 0)
    #From the subdesign, you can determine the probability
    #the rest of the system is in a given state. Using
    #This, you can comput the probability that you will
    #do an election with those processes.
    sub_design = design(procs, p)
    if sub_design == None:
        return []
    #An election can have lots of different outcomes, but
    #the list of outcomes is decided by the number and sizes
    #of the groups. Get the steady state of the sub design.
    if procs != 1:
        sub_design = correct_design(sub_design)
        T = pykov.Chain(sub_design)
        #power = 1/(p**3)
        power = MIXINGVALUE
        #print "POWER: {}".format(power)
        v = pykov.Vector()
        v[1] = 1.0
        ss = T.pow(v,int(power))
        #ss = T.steady()
    else:
        ss = {1:1}
    #ss yields a partial state. You need to keep yielding
    #partial states until you have enoigh to describe the
    #remainder of the system.
    result = []
    for config in ss:
        if config < procs:
            for subconfig in sys_config(procs-config, p):
                # Subconfig is a tuple of (config and probability)
                # Any subconfig can be combined config to yield
                # a config of size procs.
                sconf, sp = subconfig
                # so we combine the config with the subconfig
                result.append( ([config]+sconf, sp * ss[config]) ) 
        else:
            result.append( ([config], ss[config]) )
    return result
   
def detection(lgroup, p):
    # For processes in the leaders group, each of them does an
    # AYC/AYT exchange to stay in the group.
    # then each of those groups go through an AYC/AYT exchange
    # before the elections start. A certain number of processes
    # will enter a state where they won't participate in the coming
    # election.
    CORRECTNESS = 0
    pingroup = lgroup-1
    fails = 0
    noparticipate = 0
    p0,p1 = p ** 3, p**4
    sp = p**SPVALUE[lgroup] #1 - (1.0 / ( 1 + (p0/(1-p1))))
    fp = 1 - sp
    d = {}
    for combo in itertools.product([True,False], repeat=pingroup):
        stay = 0
        leave = 0
        stayp = 1
        for p in combo:
            if p:
                stay += 1
                stayp *= sp
            else:
                stayp *= fp
        try:
            d[stay] += stayp
        except KeyError:
            d[stay] = stayp
        CORRECTNESS += stayp
    r = []
    for stay in d:
        r.append( (stay+1, pingroup-stay,d[stay]) )
    assert abs(1-CORRECTNESS) < 0.00001
    return r
   
def election_outcomes(leaders, p):
    sp = (p ** 4) * (p ** 2)
    fp = 1 - sp
    r = []
    for combo in itertools.product([True, False], repeat=leaders):
        gp = sp ** sum([ 1 for c in combo if c ])
        bp = fp ** sum([ 1 for c in combo if not c])
        r.append( (combo,gp*bp) )
    return r
  
def transition(lgroup, config, p):
    #param lgroup integer - size of the leaders group
    #param config list of integers - size of each other group in the system.
    #This is a list of all AYC/AYT outcomes for the leaders group
    #print "LGROUP: {}".format(lgroup)
    #print "CONFIG: {}".format(config)
    ldrs = detection(lgroup, p)
    cmb = [ ]
    # For each group in the configuration, make a list of AYC/AYT outcomes.
    # Result will be in the form (stay, leave, probabilty)
    for group in config:
        grps = detection(group, p)
        #print "GRPS {}".format(grps)
        cmb.append(grps)
    ds = {}
    #print "CMB {}".format(cmb)
    # For each possible AYC/AYT result for each group create the product
    # To get all possible interleavings of successes & failures.
    for combo in itertools.product( *cmb ):
        # Combo is a tuple of type ((stay, leave, p), (stay, leave, p)...)
        #print "COMBO {}".format(combo)
        for ldr in ldrs:
            # For each remaining group, check to see if the election succeeds.
            ele = election_outcomes(len(config),p)
            # outcome will be a T,F list of if the groups will join with the leader
            # outp is the chance that happens
            for outcome, outp in ele:
                #print "OUTCOME {}".format(outcome)
                #print "OUTP {}".format(outp)
                solos = ldr[1] # Processes that leave the leader's group
                mygroup = ldr[0] # The processes in my group to start
                mygroup_p = outp*ldr[2] # The probability this election works
                r = zip(outcome,combo) # Mapping it with each possible leader's observed procs
                for sr in r:
                    #print "SR: {}".format(sr)
                    if sr[0]:
                        mygroup += sr[1][0]
                    mygroup_p *= sr[1][2]
                    solos += sr[1][1]
                    # Do I care about the solos, other than that they won't participate?
                try:
                    ds[mygroup] += mygroup_p
                except KeyError:
                    ds[mygroup] = mygroup_p
    rlist = []
    for group in ds:
        rlist.append( (group, ds[group]) )
    #print rlist
    return rlist
   
def design(procs, p):
    #print "DESIGN: {}".format(procs)
    if procs == 0:
        return None
    if procs == 1:
        return {(1,1):1}
    if procs == 2:
        return project_transitions(p)
    else:
        trans = {}
        for others in range(procs):
            #print "OTHERS: {}".format(others)
            #Others sets the source and size of the main group
            main_group = procs-others
            if others > 0:
                remain = sys_config(others,p)
            else:
                remain = []

            #print "REMAIN: {}".format(remain)
            # The transistion function gets back a transition for the given
            # other groups state. You take that transition and multiply it
            # by the probability the system is in that state.
            goneto = {}
            if remain:
                for (conf,confp) in remain:
                    for dest, destp in transition(main_group, conf, p):
                        #print "DEST: {}".format(dest)
                        try:
                            goneto[dest] += destp * confp
                        except KeyError:
                            goneto[dest] = destp * confp
            else:
                mg_change = detection(main_group, p)
                #print "MGCHANGE: {}".format(mg_change)
                for stay, _, stayp in mg_change:
                    try:
                        goneto[stay] += stayp
                    except KeyError:
                        goneto[stay] = stayp
            #print "GONETO: {}".format(goneto)
            for dest in goneto:
                try:
                    trans[ (main_group, dest) ] += goneto[dest]
                except KeyError:
                    trans[ (main_group, dest) ] = goneto[dest]
    #SOMETIMES WE ARE PICKING UP TEENY TINY ITTY BITTY BITS OF ERROR (Ugh)
    trans = correct_design(trans)
    return trans

def correct_design(d):
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
    
    # for each row
    for s in vd:
        diff = 1.0-vd[s]
        # Confirm that the error from the model is less than EPSILON
        #print diff
        assert(abs(diff) < EPSILON)
        # Anything less is residue from float multiplies and we'll just
        # correct for them the to get rid of them.
        if diff > 0.0:
            d[f,t] -= diff
        if diff < 0.0:
            d[f,t] += diff
    return d
        
def verify_design(d):
    vd = {}
    for (f,t) in d:
        try:
            vd[f] += d[(f,t)]
        except KeyError:
            vd[f] = d[(f,t)]
    for s in vd:
        print "VERIFY {}: {}".format(s,1.0-vd[s])
        
            
            
            
            
#print design(4,.65) 
