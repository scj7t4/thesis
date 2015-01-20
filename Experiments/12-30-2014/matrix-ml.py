# Author: Stephen Jackson
# Date: 12-18-2014
# Processes log files

import sys
import json
import pykov

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
    chain_dict = {
        ('Solo','Interim') : si,
        ('Solo','Solo')    : 1-si,
        ('Interim','Group'): ig, 
        ('Interim','Solo') : 1-ig,
        ('Group','Group')  : gg,
        ('Group','Solo')   : 1-gg,
    }
    return chain_dict

def process_log():
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
                        last_normal = 10
                    if last_size == 1 or last_size == None:
                        pair = (last_normal, last_c, "S")
                    else:
                        pair = (last_normal, last_c, "G")
                    exp_log.append(pair)
                    last_size = None
                    last_normal = None
                    #print "{}: {}".format(stage, exp_log)
                    try:
                        results[stage].append(exp_log)
                    except KeyError:
                        results[stage] = [ exp_log ]
            else:
                # This line is an entry from the log
                try:
                    (counter, state, leader, size) = line.split()
                    size = int(size)
                    counter = int(counter)
                except ValueError:
                    #print "Skipping: {}".format(line)
                    continue
                if counter < 100:
                    continue
                if state == "NORMAL":
                    #print line,
                    if last_size == None: # First normal
                        last_size = size
                        last_normal = counter
                        #print "START: {} {}".format(size,counter)
                    else:
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
        print "R {}".format(i)
        solo_stay = 0
        s = 0
        group_stay = 0
        group1_solo = 0
        g1 = 0
        g = 0
        last_state = None
        # For each log in the results set
        for log in results[i]:
            #print log
            # For each entry in the log
            for (b,e,t) in log:
                # If the state is solo
                last_state = t
                #print t
                if t == 'S':
                    # The chain didn't transition from solo for e-b ticks
                    solo_stay += e-b-1
                    s += e-b
                else:
                    # The system entered the group 1 state
                    g1 += 1
                    # The system when to group1, but went to solo.
                    # Every other transition succeeded
                    if e-b <= 1:
                        group1_solo += 1
                    else:
                        # The number of ticks that the system spent in the group state
                        group_stay += e-b-2
                        g += e-b-1
            if last_state == 'S':
                solo_stay += 1
            else:
                group_stay += 1   
        #print "+==+"
        #print solo_stay
        #print s
        #print group_stay
        #print g
        #print group1_solo
        #print g1 
        ss = solo_stay/(s*1.0)
        try:
            gg = group_stay/(g*1.0)
        except ZeroDivisionError:
            gg = 0
        try:
            igs = group1_solo/(g1*1.0)
        except ZeroDivisionError:
            igs = 1
        chain_dict = {
            ('Solo','Interim') : s-solo_stay,
            ('Solo','Solo')    : solo_stay,
            'Solo': s,
            ('Interim','Group'): g1-group1_solo, 
            ('Interim','Solo') : group1_solo,
            'Interim': g1,
            ('Group','Group')  : group_stay,
            ('Group','Solo')   : g-group_stay,
            'Group': g,
        }
        out[i/100.0] = chain_dict
         
        #print "{}\t{}".format(i,chain_dict)
    return out

def chi_test(pre, obv, t):
    s = 0
    for key in pre:
        (s1,s2) = key
        if s1 != t:
            continue
        p = pre[key]
        o = obv[key]
        p *= obv[s1]
        if p == 0:
            continue
        s += ((p-o)**2)/p
    return s

def chi_test_steady(pre, obv):
    s = 0
    t = 0
    for key in ["Solo", "Interim", "Group"]:
        t += obv[key]
    for key in pre:
        if pre[key] == 0:
            assert pre[key] == obv[key]
            continue
        p = pre[key]
        o = obv[key]
        p *= t
        s += ((p-o)**2)/p
    return s

def do_chi_trans(p, obv):
    predicted[p] = make_chain(p)
    print json.dumps(jsonify(observed[p]),indent=2)
    print json.dumps(jsonify(predicted[p]), indent=2)
    for t in ["Solo", "Interim", "Group"]:
        print "{}\t{}\t{}".format(t,p,chi_test(predicted[p], observed[p],t))

def do_chi_steady(p, obv):
    T = pykov.Chain(make_chain(p))
    pv =pykov.Vector(Solo=1)
    #ss = T.pow(pv,300)
    ss = T.steady()
    pre = {'Solo': ss['Solo'],
           'Interim': ss['Interim'],
           'Group': ss['Group']
    }
    print pre
    return chi_test_steady(pre,obv[p]) 

def jsonify(di):
    do = {}
    for key in di:
        do[str(key)] = di[key]
    return do

def main():
    r = process_log()
    observed = trans_matrix(r)
    predicted = {}
    for i in range(0,105,5):
        p = i/100.0
        print p
        print do_chi_steady(p,observed)

if __name__ == "__main__":
    main()
