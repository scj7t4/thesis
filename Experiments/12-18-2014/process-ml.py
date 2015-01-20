# Author: Stephen Jackson
# Date: 12-18-2014
# Processes log files

import sys
import json

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

def main():
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
                    exp_log = []
                elif line.find("STOP") != -1:
                    spl = line.split()
                    last_c = int(spl[4])
                    if last_size == 1:
                        pair = (last_normal, last_c, "S")
                    else:
                        pair = (last_normal, last_c, "G")
                    exp_log.append(pair)
                    last_size = None
                    last_normal = None
                    print "{}: {}".format(stage, exp_log)
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
                    print "Skipping: {}".format(line)
                    continue
                if state == "NORMAL":
                    if last_size == None: # First normal
                        last_size = size
                        last_normal = counter
                    else:
                        if size == last_size:
                            if size == 2:
                                # Member left and then group reformed
                                pair = (last_normal, counter-1, "G")
                                pair2 = (counter-1, counter, "S")
                                last_size = size
                                last_normal = counter
                                exp_log.append(pair)
                                exp_log.append(pair2)
                            elif size == 1:
                                #The group size didn't change, an election
                                #failed.
                                pass
                        elif size > last_size:
                            # Group got bigger. This was a period w/o
                            # A group
                            pair = (last_normal, counter, "S")
                            last_size = size
                            last_normal = counter
                            exp_log.append(pair)
                        else:
                            # Group got smaller. This was a period w/
                            # A group
                            pair = (last_normal, counter, "G")
                            last_size = size
                            last_normal = counter
                            exp_log.append(pair)

    for i in range(0,105,5):
        ss = 0
        sg = 0
        for log in results[i]:
            s,g = log_to_pct(log)            
            print "{} => S({}) G({})".format(i,s,g)
            ss += s
            sg += g
        print "{} AVG S({}) G({})".format(i,ss/5,sg/5)

if __name__ == "__main__":
    main()
