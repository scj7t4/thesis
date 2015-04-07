# This program should enumerate a Markov chain for a model of a given size and all of
# it's states.

class GroupState(object):
    def __init__(self, size):
        self.size = size
    
    def __repr__(self):
        return "Group{}".format(size)
    
    def __str__(self):
        return self.__repr__()

    def next_states(self, max_size):
        r = []
        for i in range(self.size-1):
            r.append(FailState(i+1))
        for i in range(self.size,max_size):
            j = i - self.size()  
            r.append(InterimState(i+1, j+1)
        r.append(self)
        return r

class InterimState(object):
    def __init__(self, group_size, pending_count):
        # group_size is how big the group will be if they all join
        # pending_count is the number of processes that might join
        self.size = group_size
        self.pending = pending_count
    
    def __repr__(self):
        return "Interim{}-Group{}".format(self.size, self.pending)
    
    def __str__(self):
        return self.__repr__()

    def next_states(self, max_size):
        # A pending state can go to any other pending state.
        r = []
        for i in range(max_size)
            for j in range(i-1)
                r.append(InterimState(i,j))
        # You can also end up in your group
        r.append(GroupState(self.size))
        

class FailState(object):
    def __init__(self, group_size):
        # This keeps track of when a member might not recognize they have been
        # removed from the group.
        self.size = group_size

    def __repr__(self):
        return "Fail-Group{}".format(self.size)
    
    def __str__(self):
        return self.__repr__()

    def next_states(self, max_size):
        # You can either go to the base group state for your size or ANY of the interim states.
        r = []
        for i in range(max_size)
            for j in range(i-1)
                r.append(InterimState(i,j))
        # You can also end up in your group
        r.append(GroupState(self.size))

def chain(max_group_size):
    basic_states = [ "Group{}".format(i+1) for i in range(max_group_size) ]
    interim_states = [ "Interim{}-Group{}".format(i+1, j+1) for i in range(max_group_size) for j in range(max_group_size) if i <= j ]
    fail_states = [ "Group{}-Fail".format(i+1) for in range(max_group_size-1) ]
    all_states = basic_states + interim_states + fail_states
    connect_matrix = 
