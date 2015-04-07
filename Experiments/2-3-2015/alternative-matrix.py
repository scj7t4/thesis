import sys
from chain import project_transitions
import json
import pykov
import math

STATES = ["Solo", "Group"]

def tokenize_log(fname):
    stages = {}
    stage = 0
    with open(fname) as fp:
        current_exp = []
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
                    current_exp = []
                elif line.find("STOP") != -1:
                    (tick, state, leader, size, fn) = current_exp[-1]
                    spl = line.split()
                    stoptick = int(spl[4])
                    current_exp.append( (stoptick, state, leader, size, fn) )
                    try:
                        stages[stage/100.0].append(current_exp)
                    except KeyError:
                        stages[stage/100.0] = [current_exp]
            else:
                try:
                    (tick, state, leader, size, fn) = line.split('\t')
                    current_exp.append( (int(tick), state, leader, int(size), fn) )
                except ValueError:
                    continue # This is an unusable startup entry.
    return stages

def exp2stream(exp):
    result = []
    exp = list(exp)
    pstate = exp.pop(0)
    for s in exp:
        (ptick, pstate, pleader, psize, fn) = pstate
        (tick, state, leader, size, fn) = s
        token = (pstate, psize)
        duration = tick-ptick
        for _ in range(duration):
            result.append(token)
        pstate = s
    return result

def convertstream(stream):
    stream = list(stream)
    result = []
    for s in stream: 
        if s[1] == 2:
            result.append('Group')
        elif s[1] == 1:
            result.append('Solo')
    return result

def stream2matrix(stream):
    matrix = {}
    stream = list(stream)
    f = stream.pop(0)
    for token in stream:
        try:
            matrix[(f,token)] += 1
        except KeyError:
            matrix[(f,token)] = 1
        f = token
    return matrix

def log_test_steady(pre, steady, obv):
    D = 0
    for i in STATES:
        for j in STATES:
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
    x2 = 0
    for i in STATES:
        for j in STATES:
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
    pre = project_transitions(p)
    print json.dumps(jsonify(observed),indent=2)
    print json.dumps(jsonify(pre), indent=2)
    return chi_test(pre, observed)

def do_log_steady(p, obv):
    pre = project_transitions(p)
    T = pykov.Chain(pre)
    pv =pykov.Vector(Solo=1)
    #ss = T.pow(pv,300)
    ss = T.steady()
    steady = {'Solo': ss['Solo'],
           'Group': ss['Group'],
    }
    print pre
    return log_test_steady(pre,steady,obv) 

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

def statecount(observed):
    r = {}
    for i in STATES:
        for j in STATES:
            if (i,j) not in observed:
                observed[(i,j)] = 0

    for (f,t) in observed:
        try:
            r[f] += observed[(f,t)]
        except KeyError:
            r[f] = observed[(f,t)]
    observed.update(r)
    return observed

def main():
    stages = tokenize_log(sys.argv[1])
    predicted = {}
    for i in range(5,100,5):
        p = i/100.0
        stream = exp2stream(stages[p][0])
        stream = convertstream(stream)
        observed = stream2matrix(stream) 
        observed = statecount(observed)
        print p
        print "CHI-SQUARE: {}".format(do_chi_trans(p,observed))
        print "LOG-LIKELY: {}".format(do_log_steady(p, observed))
    #tabularize(observed)


if __name__ == "__main__":
    main()
