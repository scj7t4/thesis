import random

GROUPCOUNTER = 0

def newgid():
    global GROUPCOUNTER
    GROUPCOUNTER += 1
    return GROUPCOUNTER
    
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
            self.connmgr.channel(self.uuid,self.leader).send(self.leader, ("AreYouThere", self.uuid))

    def merge(self):
        self.pending = []
        groupchange = False
        if self.is_leader():
            for peer in self.expected:
                if peer in self.group:
                    print "LEADER REMOVE {}".format(peer)
                    self.group.remove(peer)
                    groupchange = True
            for peer in self.coordinators:
                if peer in self.group:
                    print "LEADER REMOVE {}".format(peer)
                    self.group.remove(peer)
                    groupchange = True
            if groupchange:
                print "LEADER READY {}".format(self.group)
                self.ready()
            if not self.coordinators or min(self.coordinators) > self.uuid:
                for peer in self.coordinators:
                    self.connmgr.channel(self.uuid,peer).send(peer, ("Invite", self.groupid))
        elif self.expected:
            print "DEPARTURE"
            print self.expected
            self.recover()

    def ready(self):
        if self.pending:
            self.group = self.pending
            for peer in self.group:
                self.connmgr.channel(self.uuid,peer).send(peer, ("Ready", list(self.group)))

    def is_leader(self):
        return self.leader == self.uuid

    def read(self):
        readsome = False
        for peer in self.connmgr.peers:
            if peer == self.uuid:
                continue
            for msg in self.connmgr.channel(self.uuid,peer).read(peer):
                print "From: {} To: {} : {}".format(peer, self.uuid, msg)
                self.receive(peer,msg)        
                readsome = True
        return readsome
    
    
    def receive(self, sender, message):
        if random.random() >= self.p:
            print "DROPPED"
            return
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
            self.connmgr.channel(self.uuid,sender).send(sender, ("AYTResponse", resp))
                
        elif message[0] == "Invite":
            assert(self.leader == self.uuid)    
            if self.coordinators and sender == min(self.coordinators) and sender < self.uuid:
                self.pendingid = message[1]
                self.connmgr.channel(self.uuid,sender).send(sender, ("Accept", list(self.group)))

        elif message[0] == "Accept":
            self.pending.append(sender)
            self.pending += message[1]

        elif message[0] == "Ready":
            self.leader = sender
            self.group = message[1]
            self.groupid = self.pendingid
    
        elif message[0] == "AYCResponse":
            self.expected.remove(sender)
            if message[1]:
                self.coordinators.append(sender) 

        elif message[0] == "AYTResponse":
            self.expected.remove(sender)
            if not message[1]:
                self.expected.append(self.uuid)

        else:
            raise ValueError("Unhandled message type {}".format(message[0]))

def observe(obs):
    d = {}
    prev = obs[0]
    for o in obs[1:]:
        try:
            d[(prev,o)] += 1
        except KeyError:
            d[(prev,o)] = 1
        prev = o
    return d
    
def chainify(obs):
    states = []
    statetot = {}
    for k,_ in obs:
        states.append(k)
        statetot[k] = 0
    for k,k2 in obs:
        statetot[k] += obs[(k,k2)]
    print statetot
    mkov = {}
    for k,k2 in obs:
        mkov[(k,k2)] = obs[(k,k2)]/(statetot[k]*1.0)
    return mkov
    
def pretty(d):
    for k in d:
        print "{} : {}".format(k,d[k])

def make_chain():
    cm = ConnectionManager()
    procs = [ GM(x,cm,p=p) for (x,p) in zip("ABCDE",[.65]*5) ]
    print procs
    observations = []
    for _ in range(100000):
        for p in procs:
            p.check()
        readuntilempty(procs)
        for p in procs:
            p.merge() 
        readuntilempty(procs)
        for p in procs:
            p.ready()  
        readuntilempty(procs)
        print procs
        observations.append( len(procs[0].group)+1 )
    print observations
    o = observe(observations)
    print o
    c = chainify(o)
    pretty(c)
    return c
    
if __name__ == "__main__":
    print make_chain()