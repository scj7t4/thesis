import random
import logging
import numpy as np
import pickle

from collections import deque

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
    order = list(procs)
    random.shuffle(order)
    while any([ p.read() for p in order]):
        random.shuffle(order)
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
        #self.expected = []
        self.pendingid = 0
        self.pendingldr = self.uuid
        self.sawayc = False    
    
    def __repr__(self):
        return "PROC {} - G({}): {} L: {}".format(self.uuid, self.groupid, self.group, self.leader)

    def check(self):
        self.sawayc = False
        self.expected = []
        self.coordinators = []
        self.groupchange = False
        self.pendingldr = self.uuid
        self.pendingid = 0
        if self.is_leader():
            for peer in self.connmgr.peers:
                if self.uuid == peer:
                    continue
                self.connmgr.channel(self.uuid,peer).send(peer, {'msg': "AreYouCoordinator"})
                self.expected.append(peer)
        else:
            for peer in self.connmgr.peers:
                if peer >= self.uuid:
                    continue
                if peer == self.leader:
                    continue
                self.connmgr.channel(self.uuid,peer).send(peer, {'msg': "AreYouCoordinator"})
                self.expected.append(peer)
            self.expected.append(self.leader)
            self.connmgr.channel(self.uuid,self.leader).send(self.leader, {'msg':"AreYouThere", 'groupid': self.groupid})
            #print "Member {} expects {}".format(self.uuid, self.expected)

    def merge(self):
        self.pending = []
        groupchange = False
        if self.is_leader() and self.pendingldr >= self.uuid:
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
            if self.coordinators:
                self.pendingid = newgid()
                self.pendingldr = self.uuid
                for peer in self.coordinators:
                    if peer in self.expected:
                        continue
                    if peer < self.uuid:
                        continue
                    self.connmgr.channel(self.uuid,peer).send(peer, {'msg': "Invite", 'pendingid': self.pendingid, 'leader': self.uuid})
                self.pending = list(self.group)
        elif self.leader in self.expected:
            #self.recover()
            pass
        self.expected = []

    def ready(self):
        self.expected = []
        # Always send ready
        if self.is_leader() and self.pendingldr == self.uuid:
            oldgroup = list(self.group)
            if self.pending:
                self.group = list(set(self.pending))
                self.groupid = self.pendingid
            else:
                self.group = list(set(self.group))
            if self.uuid in self.group:
                self.group.remove(uuid)
            self.expected = list(self.group)
            for peer in self.group:
                self.connmgr.channel(self.uuid,peer).send(peer, {'msg': "Ready", 'groupid': self.groupid, 'members': list(self.group)})
    
    def cleanup(self):
        if self.is_leader():
            for p in self.expected:
                self.group.remove(p)
        self.expected = []
        self.coordinators = []
        self.pending = []
        self.pendingldr = self.uuid
        self.pendingid = 0
        #if self.sawayc == False:
        #    self.recover()

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
        drop = np.random.binomial(1, 1.0-self.p)
        dbg = "MSG F: {} T: {} -- {} {}".format(sender, self.uuid, message, "!! Dropped" if drop else ""),
        logging.debug(dbg)
        if drop:
            return
        if 'msg' not in message:
            raise KeyError("Bad message {}".format(message))
        if message['msg'] == "AreYouCoordinator":
            if self.is_leader():
                resp = True
            else:
                resp = False
            self.connmgr.channel(self.uuid,sender).send(sender, {'msg':"AYCResponse",'resp':resp, 'leader': self.leader})

        elif message['msg'] == "AreYouThere":
            if sender in self.group:
                resp = True
            else:
                resp = False
                self.coordinators.append(sender)
            self.connmgr.channel(self.uuid,sender).send(sender, {'msg': "AYTResponse", 'resp': resp, 'groupid': self.groupid, 'members': list(self.group)})
                
        elif message['msg'] == "Invite":
            if ((sender < self.uuid) and (message['leader'] <= self.leader)
             and (self.pendingldr > message['leader']) and (sender in self.coordinators)):
                self.pendingid = message['pendingid']
                self.pendingldr = message['leader']
                self.connmgr.channel(self.uuid,sender).send(sender, {'msg': "Accept"})

        elif message['msg'] == "Accept":
            self.pending.append(sender)
            # l = list(message[1])
            # if self.uuid in l:
            #   l.remove(self.uuid)
            # self.pending += l

        elif message['msg'] == "Ready":
            if self.pendingldr == sender or self.leader == sender:
                self.leader = sender
                self.group = list(message['members'])
                self.groupid = message['groupid']
                assert(not self.is_leader() or self.groupid == self.pendingid)
                self.connmgr.channel(self.uuid,sender).send(sender, {'msg': "ReadyAck", 'groupid': self.groupid})
            else:
                #ignore, this isn't the best process.
                pass
    
        elif message['msg'] == "AYCResponse":
            #print "{} r-expects {}".format(self.uuid, self.expected)
            self.expected.remove(sender)
            if message['leader'] != self.uuid:
                if sender in self.group:
                    self.group.remove(sender)
                self.coordinators.append(sender) 

        elif message['msg'] == "AYTResponse":
            self.expected.remove(sender)
            if not message['resp']:
                self.recover()
                self.coordinators.append(sender)
            else:
                self.groupid = message['groupid']
                self.group = list(message['members'])
        
        elif message['msg'] == "ReadyAck":
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

def mkv_state(syst):
    return len(syst[0].group)+1

def sys_state(syst):
    return tuple([ tuple(x.group) for x in syst])

def make_chain_2(procs, prob, applications=10):
    cm = ConnectionManager()
    syst = [ GM(x,cm,p=p) for (x,p) in zip(range(procs),[prob]*procs) ]
    queue = deque([])
    states = set()
    states.add(sys_state(syst)) 
    queue.append(pickle.dumps(syst))
    observations = []
    c = 0
    while queue:
        c += 1
        if c % 10 == 0:
            print "c={} q={}".format(c,len(queue)) 
        pick = queue.popleft()
        for _ in range(applications):
            syst = pickle.loads(pick)
            ob = mkv_state(syst)
            observations.append(ob)
            applyonce(syst)
            ob = mkv_state(syst)
            observations.append( ob )
            observations.append('X')
            if sys_state(syst) not in states:
                states.add(sys_state(syst))
                queue.append(pickle.dumps(syst))
    o = observe(observations)
    pretty(o)
    c = chainify(o)
    pretty(c)
    return (o, likely_observe(observations))
 
def make_chain(procs,prob,sets=1,iters=10000):
    observations = []
    for _ in range(sets):
        cm = ConnectionManager()
        syst = [ GM(x,cm,p=p) for (x,p) in zip(range(procs),[prob]*procs) ]
        observations.append(1)
        for __ in range(iters):
            logging.info(str(syst))
            applyonce(syst)
            ob = len(syst[0].group)+1
            # if ob == 2 and True:
                # with open('scenario.pickle','w+') as cfp:
                    # pickle.dump(syst, cfp)
                # exit()
            observations.append( ob )
        logging.info(str(syst))
        observations.append('X')
        

    o = observe(observations)
    pretty(o)
    c = chainify(o)
    pretty(c)
    return (o, likely_observe(observations))
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    make_chain(5,0.75)
