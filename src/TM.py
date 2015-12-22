"""
Program name: PIP/GPS interpreter
Module description: General transition matrix
Date: 22.12.2014
Authors:
    Grankovskiy P. A.
    Polikarpov V. N.
    Shtern A. N.
"""

class Matrix:
    def __init__(self, terms, matrix):
        self.table = {}
        for head, funcs in matrix.items():
            d = {}
            for term, func in zip(terms, funcs):
                d[term] = func
            self.table[head] = d
    def action(self, head, term):
        return self.table[head][term]

class TM:
    def __init__(self, matrix, terms, funcarr, table, initfunc):
        self.matrix = Matrix(terms, matrix)
        self.arr = funcarr
        self.table = table
        self.initfunc = initfunc
        self.stack = []
        self.cur = ''

    def run(self, inp):
        self.inp = inp
        self.initfunc()
        ret = None
        while not ret:
            ret = self.step()
        return ret

    def read(self):
        if self.inp:
            self.c = self.inp.pop(0)
        else:
            self.c = None
        #print(self.table.name(self.c) if self.c else self.c)
        return self.c

    def step(self):
        func = self.matrix.action(self.stack[-1].text, self.table.name2(self.c))
        #print(self.stack, self.table.name2(self.c) if self.c else self.c, func)
        return self.arr[func]()
        
