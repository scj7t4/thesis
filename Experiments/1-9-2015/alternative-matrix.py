import sys

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
                    (tick, state, leader, size) = current_exp[-1]
                    spl = line.split()
                    stoptick = int(spl[4])
                    current_exp.append( (stoptick, state, leader, size) )
                    try:
                        stages[stage/100.0].append(current_exp)
                    except KeyError:
                        stages[stage/100.0] = [current_exp]
            else:
                try:
                    (tick, state, leader, size) = line.split()
                    current_exp.append( (int(tick), state, leader, int(size)) )
                except ValueError:
                    continue # This is an unusable startup entry.
    return stages

def exp2stream(exp):
    result = []
    exp = list(exp)
    pstate = exp.pop(0)
    for s in exp:
        (ptick, pstate, pleader, psize) = pstate
        (tick, state, leader, size) = s
        token = (pstate, psize)
        duration = tick-ptick
        for _ in range(duration):
            result.append(token)
        pstate = s
    return result

def convertstream(stream):
    stream = list(stream)
    result = []
    p = 1
    for s in stream: 
        if p == 1 and s[1] == 2:
            result.append('Interim')
        elif s[1] == 2:
            result.append('Group')
        elif s[1] == 1:
            result.append('Solo')
        p = s[1]
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

stages = tokenize_log(sys.argv[1])
stream = exp2stream(stages[0.95][0])
stream = convertstream(stream)
print stream2matrix(stream)
