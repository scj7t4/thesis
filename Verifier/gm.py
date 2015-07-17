import random

GROUPCOUNTER = 0

def newgid():
    global GROUPCOUNTER
    GROUPCOUNTER += 1
    return GROUPCOUNTER
   
MINLEADER = 0
 
class ConnectionManager(object):
    def __init__(self):
        self.connections = {}
        self.peers = set()    

    def channel(self, uuida, uuidb):
        t1 = min(uuida,uuidb)
        t2 = max(uuida,uuidb)
        if (t1,t2) not in self.connections:
            self.add_peer(uuida)
            self.add_peer(uuidb)
            c = Connection(t1, t2)
            self.connections[(t1,t2)] = c
        return self.connections[(t1,t2)]

    def add_peer(self,uuid):
        self.peers.add(uuid)
        
class Connection(object):
    def __init__(self, uuida, uuidb):
        self.channela = []
        self.uuida = min(uuida,uuidb)
        self.channelb = []
        self.uuidb = max(uuida,uuidb)

    def send(self, dest, msg):
        if self.uuida == dest:
            dest = self.channela
        else:
            dest = self.channelb
        dest.append(msg)
        
    def read(self, dest):
        if self.uuida == dest:
            dest = self.channelb
        else:
            dest = self.channela
        while len(dest):
            yield dest.pop(0)
            
def readuntilempty(procs):
    while any([ p.read() for p in procs]):
        pass

class GM(object):
    def __init__(self, uuid, connmgr, p=1.0):
        self.uuid = uuid
        self.connmgr = connmgr
        connmgr.add_peer(uuid)
        self.recover()
        self.p = p
        
    def recover(self):
        #print "{} RECOVERS".format(self.uuid)
        self.leader = self.uuid
        self.group = []
        self.groupid = newgid()
        self.coordinators = []
        self.pending = []
        self.expected = []
        self.pendingid = 0
        
    def __repr__(self):
        return "PROC {} - G({}): {} L: {}".format(self.uuid, self.groupid, self.group, self.leader)

    def check(self):
        self.expected = []
        self.coordinators = []
        self.groupchange = False
        if self.is_leader():
            for peer in self.connmgr.peers:
                if self.uuid == peer:
                    continue
                self.connmgr.channel(self.uuid,peer).send(peer, ("AreYouCoordinator", self.uuid))
                self.expected.append(peer)
        else:
            self.expected.append(self.leader)
            self.connmgr.channel(self.uuid,self.leader).send(self.leader, ("AreYouThere", self.groupid))

    def merge(self):
        self.pending = []
        groupchange = False
        if self.is_leader():
            for peer in self.expected:
                if peer in self.group:
                    self.group.remove(peer)
                    groupchange = True
            for peer in self.coordinators:
                if peer in self.group:
                    self.group.remove(peer)
                    groupchange = True
            #if groupchange:
            #    self.ready()
            self.pendingid = newgid()
            if not self.coordinators or min(self.coordinators) > self.uuid:
                for peer in self.coordinators:
                    if peer in self.expected:
                        continue
                    self.connmgr.channel(self.uuid,peer).send(peer, ("Invite", self.pendingid))
                self.pending = list(self.group)
        elif self.expected:
            #self.recover()
            pass

    def ready(self):
        self.expected = []
        if self.pending and self.pending != self.group:
            oldgroup = list(self.group)
            self.group = list(self.pending)
            self.group = list(set(self.group))
            self.groupid = self.pendingid
            if self.uuid in self.group:
                self.group.remove(uuid)
            self.expected = list(self.group)
            #print "OLD {} NEW {} EXPECTED {}".format(oldgroup, self.group, self.expected)
            for peer in oldgroup:
                self.expected.remove(peer)
            for peer in self.group:
                self.connmgr.channel(self.uuid,peer).send(peer, ("Ready", self.groupid, list(self.group)))
    
    def cleanup(self):
        if self.is_leader():
            for p in self.expected:
                self.group.remove(p)
        self.expected = []
        self.coordinators = []
        self.pending = []

    def is_leader(self):
        return self.leader == self.uuid

    def read(self):
        readsome = False
        for peer in self.connmgr.peers:
            if peer == self.uuid:
                continue
            for msg in self.connmgr.channel(self.uuid,peer).read(peer):
                #print "From: {} To: {} : {}".format(peer, self.uuid, msg)
                self.receive(peer,msg)        
                readsome = True
        return readsome
    
    
    def receive(self, sender, message):
        prnt = False #self.uuid == 0 or sender == 0
        if prnt:
            print "MSG F: {} T: {} -- {}".format(sender, self.uuid, message),
        if random.random() >= self.p:
            if prnt:
                print " !! Dropped"
            return
        else:
            if prnt:
                print ""
            pass
        if message[0] == "AreYouCoordinator":
            if self.is_leader():
                resp = True
            else:
                resp = False
            self.connmgr.channel(self.uuid,sender).send(sender, ("AYCResponse", resp))

        elif message[0] == "AreYouThere":
            if sender in self.group:
                resp = True
            else:
                resp = False
                self.coordinators.append(sender)
            self.connmgr.channel(self.uuid,sender).send(sender, ("AYTResponse", resp, self.groupid, list(self.group)))
                
        elif message[0] == "Invite":
            if MINLEADER in self.coordinators and sender == MINLEADER: #(self.coordinators and sender == min(self.coordinators) and sender < self.uuid):
                assert(self.leader == self.uuid)    
                self.pendingid = message[1]
                self.connmgr.channel(self.uuid,sender).send(sender, ("Accept", list(self.group)))

        elif message[0] == "Accept":
            self.pending.append(sender)
            l = list(message[1])
            if self.uuid in l:
                l.remove(self.uuid)
            self.pending += l

        elif message[0] == "Ready":
            self.leader = sender
            self.group = list(message[2])
            self.groupid = message[1]
            assert(not self.is_leader() or self.groupid == self.pendingid)
            self.connmgr.channel(self.uuid,sender).send(sender, ("ReadyAck", self.groupid))
    
        elif message[0] == "AYCResponse":
            self.expected.remove(sender)
            if message[1]:
                self.coordinators.append(sender) 

        elif message[0] == "AYTResponse":
            self.expected.remove(sender)
            if not message[1]:
                self.recover()
                self.coordinators.append(sender)
            else:
                self.groupid = message[2]
                self.group = list(message[3])
        
        elif message[0] == "ReadyAck":
            if sender in self.expected:
                self.expected.remove(sender)

        else:
            raise ValueError("Unhandled message type {}".format(message[0]))

def observe(obs):
    d = {}
    prev = obs[0]
    for o in obs[1:]:
        if o == 'X':
            prev = 'X'
            continue
        if prev == 'X':
            prev = o
            continue
        try:
            d[(prev,o)] += 1
        except KeyError:
            d[(prev,o)] = 1
        prev = o
    return d

def likely_observe(obs):
    d = {}
    prev = obs[0]
    c = 0
    for o in obs[1:]:
        if o == 'X':
            prev = 'X'
            continue
        if prev == 'X':
            prev = o
            c = 0
            continue
        try:
            d[(c,prev,o)] += 1
        except KeyError:
            d[(c,prev,o)] = 1
        prev = o
        c += 1
    return d
    
def observe2nd(obs):
    d = {}
    p2 = obs[0]
    p1 = obs[1]
    for o in obs[2:]:
        try:
            d[((p2,p1),o)] += 1
        except KeyError:
            d[((p2,p1),o)] = 1
        p2 = p1
        p1 = o
    return d
        
def chainify(obs):
    states = []
    statetot = {}
    for k,_ in obs:
        states.append(k)
        statetot[k] = 0
    mkov = {}
    for k,k2 in obs:
        if k == 'X' or k2 == 'X':
            continue
        statetot[k] += obs[(k,k2)]
    for k,k2 in obs:
        if k == 'X' or k2 == 'X':
            continue
        mkov[(k,k2)] = obs[(k,k2)] / (statetot[k] * 1.0)
    return mkov

 
def pretty(d):
    for k in d:
        print "{} : {}".format(k,d[k])

def applyonce(procs):
    for p in procs:
        p.check()
    readuntilempty(procs)
    for p in procs:
        p.merge() 
    readuntilempty(procs)
    for p in procs:
        p.ready()  
    readuntilempty(procs)   
    for p in procs:
        p.cleanup()  
 
def make_chain(procs,prob):

    observations = []
    
    
    for _ in range(1):
        cm = ConnectionManager()
        syst = [ GM(x,cm,p=p) for (x,p) in zip(range(procs),[prob]*procs) ]
        observations.append(1)
        for __ in range(10000):
            #print syst
            applyonce(syst)
            observations.append( len(syst[0].group)+1 )
        #print syst
        observations.append('X')
        

    o = observe(observations)
    pretty(o)
    c = chainify(o)
    pretty(c)
    return (o, likely_observe(observations))
    
if __name__ == "__main__":
    print make_chain(3,.95)
