import itertools

def transition(p, num_procs, perspective, end_size):
    indiv_prob = {}
    if perspective == 0 and end_size == 'A':
        return 0
    elif end_size == 'A':
        prob = 1
        # Of the processes that have higher priority than you
        # Any one of them deliver you an invite AND
        # That one successfully finishes the election
        # The probability that none of them work
        prob_tmp = (1-p)**perspective
        # The probability that at least one of them works is 1-prob none work
        prob *= (1-prob_tmp)
        # Then you have to send the accept, and they have to send the ready 
        prob *= p**2
        return prob
    else:
        a_prob = transition(p, num_procs, perspective, 'A')

    for potential_mem in range(num_procs-perspective-1):
        mem_uuid = potential_mem + perspective + 1
        # Your invite arrives and all higher procs fail:
        p_inv_works = p * (1-p)**perspective
        p_rest_works = p ** 3
        indiv_prob[mem_uuid] = p_inv_works * p_rest_works
 
    final_prob = 0
    for combo in itertools.combinations(indiv_prob.keys(), end_size-1):
        tmp = 1
        for mem in combo:
            subp = indiv_prob[mem]
            tmp = tmp * subp
        for mem in indiv_prob:
            if mem in combo:
                continue
            subp = indiv_prob[mem]
            tmp = tmp * (1-subp)
        final_prob += tmp
    return final_prob * (1-a_prob)


def design(p, num_procs, perspective):
    states = range(1, num_procs-perspective+1)
    states.append('A')
    
    design = {}
    for state in states:
        for state2 in states:
            design[(state,state2)] = transition(p, num_procs, perspective, state2)
    return design

if __name__ == "__main__":
    print design(0.75, 5, 2)
