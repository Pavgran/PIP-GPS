"""
Program name: PIP/GPS interpreter
Module description: General finite state machine
Date: 22.12.2014
Authors:
    Grankovskiy P. A.
    Polikarpov V. N.
    Shtern A. N.
"""

class TransTable:
    def __init__(self, table):
        self.states = {j:i for i,j in enumerate(table.keys())}
        self.n = len(table)
        self.table = [{} for i in range(self.n)]
        for state, transitions in table.items():
            for cases, action in transitions.items():
                if not cases:
                    self.__add(state, cases, *action)
                    continue
                while ':' in cases:
                    for c in range(ord(cases[0]),ord(cases[2])+1):
                        self.__add(state, chr(c), *action)
                    cases = cases[3:]
                for c in cases:
                    self.__add(state, c, *action)
                    
    def __add(self, state, case, newstate, action):
        self.table[self.states[state]][case] = (self.states[newstate], action)
        
    def statenum(self, state):
        return self.states[state]

    def action(self, state, inp):
        if inp in self.table[state]:
            return self.table[state][inp]
        else:
            return self.table[state]['']
        
class FSM:
    def __init__(self, transtable, funcarr, initstate, initfunc):
        self.table = TransTable(transtable)
        self.arr = funcarr
        self.state = self.table.statenum(initstate)
        self.initfunc = initfunc

    def run(self, inp):
        self.inp = inp
        self.initfunc()
        ret = None
        while not ret:
            ret = self.step()
        return ret

    def read(self):
        if self.inp:
            self.c, self.inp = self.inp[0], self.inp[1:]
        else:
            self.c = None
        #print(self.c, end='')
        return self.c

    def step(self):
        self.state, func = self.table.action(self.state, self.c)
        return self.arr[func]()
        
