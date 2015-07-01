import random
import itertools

def trial(p):
    c = 0
    while 1:
        t = random.random()
        _ = random.random()
        if t <= p:
            c += 1
        else:
            break

    _ = random.random()
    _ = random.random()
    return c

TRIALS = 100000
sequence = []
for _ in range(TRIALS):
    c = trial(0.95)
    sequence.append(c)

two = 0
one = 0
zero = 0
while len(sequence) > 1:
    a = sequence.pop(0)
    b = sequence[0]
    if a >= 6 and b >= 6:
        two += 1
    elif a >= 6 or b >= 6:
        one += 1
    else:
        zero += 1

print "Two: {} ({}) One: {} ({}) Zero: {} ({})".format(two,two*1.0/TRIALS, one, one*1.0/TRIALS, zero, zero*1.0/TRIALS)