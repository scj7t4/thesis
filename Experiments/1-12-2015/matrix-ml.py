# Author: Stephen Jackson
# Date: 12-18-2014
# Processes log files

import sys
import json
import pykov
import math

def log_to_pct(log):
    solo = 0
    group = 0
    for (b,e,t) in log:
        if t == "S":
            solo += e-b
        else:
            group += e-b
    tot = solo+group*1.0
    return (solo/tot, group/tot)

def make_chain(p):
    si = p ** 6
    ig = p ** 3
    gg = p ** 4
    ii = (1-p**1) * (p**6)
    gi = (1-p**2) * (p**6)
    fi = gi
    chain_dict = {
        ('Solo','Interim') : si,
        ('Solo','Solo')    : 1-si,
        ('Interim','Group'): ig, 
        ('Interim','Solo') : 1-ig-ii,
        ('Interim','Interim'): ii,
        ('Group','Group')  : gg,
        ('Group','Failed')   : 1-gg-gi,
        ('Group','Interim'): gi,
        ('Failed', 'Solo') : 1-fi,
        ('Failed', 'Interim'): fi,
    }
    return chain_dict

def verify_log(log,skip=0):
    pt = None
    pe = None
    for (start,end,t) in log:
        print (start,end,t)
        if pt == None:
            pass
        elif pt == 'G':
            assert t == 'S'
        else:
            assert t == 'G'
        pt = t
        if pe == None:
            assert start == skip
        else:
            assert start == pe
        pe = end
        #assert start < end

def process_log(skip=0):
    stage = 0
    exp_log = []
    results = dict()
    with open(sys.argv[1]) as fp:
        last_size = None
        last_normal = None
        for line in fp:
            if line.find("##") == 0:
                # This line shows the stage that the program is on
                p = line.split('[')
                p = p[1].split(']')
                stage = int(p[0]) # Grab the reliability.              
            elif line.find("**") == 0:
                # This line will mark the start or end of a DGI run
                if line.find("START") != -1:
                    #print "!!! START {}".format(stage)
                    exp_log = []
                elif line.find("STOP") != -1:
                    spl = line.split()
                    last_c = int(spl[4])
                    if last_normal == None:
                        last_normal = skip     
                    if last_size == 1:
                        pair = (last_normal, last_c, "S")
                    else:
                        pair = (last_normal, last_c, "G")
                    exp_log.append(pair)
                    last_size = None
                    last_normal = None
                    print "{}: {}".format(stage, exp_log)
                    verify_log(exp_log,skip=skip)
                    try:
                        results[stage].append(exp_log)
                    except KeyError:
                        results[stage] = [ exp_log ]
            else:
                # This line is an entry from the log
                try:
                    spl = line.split()
                    (counter, state, leader, size, fn) = line.split('\t')
                    size = int(size)
                    counter = int(counter)
                except ValueError:
                    #print "Skipping: {}".format(line)
                    continue
                if state != "NORMAL":
                    continue
                if counter < skip and state == "NORMAL":
                    last_size = size
                    continue
                #print line,
                if last_normal == None: # First normal
                    last_normal = counter if skip == 0 else skip
                    #print "START: {} {}".format(size,counter)
                if size == last_size:
                    if size == 2:
                        #print "GROUP FROM {} to {}".format(last_normal,counter-1)
                        #print "SOLO FROM {} to {}".format(counter-1,counter)
                        # Member left and then group reformed
                        pair = (last_normal, counter, "G")
                        pair2 = (counter, counter, "S")
                        last_size = size
                        last_normal = counter
                        exp_log.append(pair)
                        exp_log.append(pair2)
                    elif size == 1:
                        #The group size didn't change, an election
                        #failed.
                        #print "FAILED ELECTION {}".format(counter)
                        pass
                elif size > last_size:
                    # Group got bigger. This was a period w/o
                    # A group
                    #print "SOLO FROM {} to {}".format(last_normal, counter)
                    pair = (last_normal, counter, "S")
                    last_size = size
                    last_normal = counter
                    exp_log.append(pair)
                else:
                    # Group got smaller. This was a period w/
                    # A group
                    #print "GROUP FROM {} to {}".format(last_normal, counter-1)
                    pair = (last_normal, counter, "G")
                    last_size = size
                    last_normal = counter
                    exp_log.append(pair)

    return results

def steady_state(results):
    print "Pct\tSolo\tGrp"
    for i in range(0,105,5):
        ss = 0
        sg = 0
        for log in results[i]:
            s,g = log_to_pct(log)            
            print "{}\t{}\t{}".format(i,s,g)
            ss += s
            sg += g
        #print "{} AVG S({}) G({})".format(i,ss/1,sg/1)

def trans_matrix(results):
    out = {}
    for i in range(0,105,5):
        chain_dict = {
            ('Solo','Interim') : 0,
            ('Solo','Solo')    : 0,
            ('Interim','Group'): 0, 
            ('Interim','Solo') : 0,
            ('Interim','Interim'): 0,
            ('Group','Group')  : 0,
            ('Group','Failed')   : 0,
            ('Group','Interim'): 0,
            ('Failed','Solo')  : 0,
            ('Failed','Interim'): 0,
            'Solo': 0,
            'Group': 0,
            'Interim': 0,
            'Failed': 0,
        }
        print "R {}".format(i)
        # For each log in the results set
        token_form = []
        # Consume entries from the log and convert it to
        # A sequence of observed states
        for log in results[i]:
            length = log[-1][1] - log[0][0] 
            pend = None
            print log
            for entry in log:
                print entry
                (start, end, token) = entry
                assert pend == None or start == pend
                pend = end
                if token == 'S':
                    dlen = end-start
                    if dlen > 0:
                        if len(token_form) > 0 and token_form[-1] != 'Interim':
                            dlen -= 1
                            token_form.append('Failed')
                        for _ in range(dlen):
                            token_form.append('Solo')
                elif token == 'G':
                    # Groups always last at least one tick, unless its the last entry
                    assert end > start or entry == log[-1] or entry == log[0]
                    if end > start:
                        dlen = end-start
                        if len(token_form) > 0:
                            token_form.append('Interim')
                            dlen -= 1
                        for _ in range(dlen):
                            token_form.append('Group')
            assert len(token_form) == length
            print token_form
            # Consume tokens and convert them into a transition frequency
            f = token_form.pop(0)
            while len(token_form):
                t = token_form.pop(0)
                chain_dict[(f,t)] += 1
                chain_dict[f] += 1
                f = t
            # Verify that everything seems good.
            checker = {'Solo': 0, 'Group':0, 'Interim': 0, 'Failed': 0}
            for key in chain_dict:
                try:
                    (s,e) = key
                    checker[s] += chain_dict[key]
                except ValueError:
                    pass
            s = 0
            for key in checker:
                s += checker[key]
                assert checker[key] == chain_dict[key]
            assert s == length-1
            out[i/100.0] = chain_dict 
            print "{}\t{}".format(i,chain_dict)
    return out

def log_test_steady(pre, steady, obv):
    states = ["Solo", "Interim", "Group", "Failed"]
    D = 0
    for i in states:
        for j in states:
            if ((i,j) not in pre):
                pfreq = 0
            else:
                pfreq = pre[(i,j)]
            try:
                ofreq = (float(obv[(i,j)]) / obv[i])
            except ZeroDivisionError:
                ofreq = 0
            except KeyError:
                continue
            if ofreq == 0:
                continue
            D += steady[i] * pfreq * math.log( pfreq / ofreq , 2 )
    return D

def chi_test(pre,obv):
    # THIS IS THE METHOD FROM THE PAPER
    states = ["Solo", "Interim", "Group", "Failed"]
    x2 = 0
    for i in states:
        for j in states:
            if ((i,j) not in pre) or (pre[(i,j)] == 0):
                assert ((i,j) not in obv) or (obv[(i,j)] == 0)  
                continue
            try:
                ofreq = (float(obv[(i,j)]) / obv[i])
            except ZeroDivisionError:
                ofreq = 0
            x2 += obv[i]*((ofreq - pre[(i,j)] )**2) / pre[(i,j)]   
    return x2

def do_chi_trans(p, observed):
    pre = make_chain(p)
    print json.dumps(jsonify(observed[p]),indent=2)
    print json.dumps(jsonify(pre), indent=2)
    return chi_test(pre, observed[p])

def do_log_steady(p, obv):
    pre = make_chain(p)
    T = pykov.Chain(pre)
    pv =pykov.Vector(Solo=1)
    #ss = T.pow(pv,300)
    ss = T.steady()
    steady = {'Solo': ss['Solo'],
           'Interim': ss['Interim'],
           'Group': ss['Group'],
           'Failed': ss['Failed'],
    }
    print pre
    return log_test_steady(pre,steady,obv[p]) 

def tabularize(result):
    print "\t".join(["p"]+ [ str(key) for key in result[0.50] ])
    for i in range(0,105,5):
        i /= 100.0
        print "\t".join([str(i)] + [ str(result[i][key]) for key in result[i] ])

def jsonify(di):
    do = {}
    for key in di:
        do[str(key)] = di[key]
    return do

def main():
    r = process_log(skip=4)
    observed = trans_matrix(r)
    predicted = {}
    for i in range(0,105,5):
        p = i/100.0
        print p
        print "CHI-SQUARE: {}".format(do_chi_trans(p,observed))
        print "LOG-LIKELY: {}".format(do_log_steady(p, observed))
    tabularize(observed)

if __name__ == "__main__":
    main()
