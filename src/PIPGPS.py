"""
Program name: PIP/GPS interpreter
Module description: Name table and interpreter
Date: 22.12.2014
Authors:
    Grankovskiy P. A.
    Polikarpov V. N.
    Shtern A. N.
"""

import FSM
import TM
import funcs
import PFAnalyzer

class Entry:
    def __init__(self, name, typ, val):
        self.name = name
        self.typ = typ
        self.val = val

class NameTable:
    def __init__(self, terms):
        self.table = {}
        self.arr = []
        self.n = 0
        self.termn = len(terms)
        for term, func in terms.items():
            self.__add(term, 'term', func)
        self.n = 0

    def __add(self, name, typ, val):
        if typ == 'term':
            self.table[name] = -self.n-1
        else:
            self.table[name] = self.n
        self.arr += [Entry(name, typ, val)]
        self.n += 1

    def addname(self, name):
        if name in self.table:
            if self.typ(self.num(name)) not in ['term', 'a']:
                raise TypeError
        else:
            self.__add(name, 'a', None)

    def addconst(self, name):
        if name in self.table :
            if self.typ(self.num(name)) != 'const':
                raise TypeError
        else:
            self.__add(name, 'const', int(name))

    def addlabel(self, name):
        if name in self.table:
            if self.typ(self.num(name)) == 'lbl':
                raise Exception("Already used label")
            elif self.typ(self.num(name)) != 'lbl':
                raise TypeError
        else:
            self.__add(name, 'lbl', None)

    def addstr(self, name):
        if name in self.table:
            if self.typ(self.num(name)) != 'str':
                raise TypeError
        else:
            self.__add(name, 'str', name[1:])

    def setval(self, num, val):
        if num < 0:
            raise TypeError
        else:
            self.arr[num+self.termn].val = val

    def settyp(self, num, typ):
        if num < 0:
            raise TypeError
        else:
            self.arr[num+self.termn].typ = typ
        
    def num(self, name):
        return self.table[name]

    def name(self, num):
        if num is None:
            return num
        if num < 0:
            return self.arr[-num-1].name
        else:
            return self.arr[num+self.termn].name

    def name2(self, num):
        if num is None:
            return num
        if num < 0:
            return self.arr[-num-1].name
        else:
            ret = self.arr[num+self.termn].typ
            if ret == 'const':
                ret = 'a'
            return ret

    def typ(self, num):
        if num < 0:
            return self.arr[-num-1].typ
        else:
            return self.arr[num+self.termn].typ

    def val(self, num):
        if num < 0:
            return self.arr[-num-1].val
        else:
            return self.arr[num+self.termn].val

    def labelval(self, num):
        name = '#'+self.name(num)
        if name in self.table:
            return self.val(self.table[name])

class PIPGPS:
    def __init__(self):
        names={
            None: None,
            '=': None,
            '+': None,
            '-': None,
            '*': None,
            '==': None,
            '>': None,
            '<': None,
            '!=': None,
            'OR': None,
            'AND': None,
            '(': None,
            ')': None,
            '{': None,
            '}': None,
            'iPHONLY': None,
            'ANDROIDLY': None,
            'GOOGLEFOR': None,
            'SMS': None,
            ';': None}
        self.table = NameTable(names)
        fsmf = funcs.FSMfuncs(self.table)
        fsmfuncs = [getattr(fsmf, 'func'+str(i)) for i in range(12)]
        self.fsm = FSM.FSM(fsmf.transtable, fsmfuncs, 'st', fsmf.read)
        fsmf.attach(self.fsm)
        
        tmf = funcs.TMfuncs()
        tmfuncs = [getattr(tmf, 'syncase'+str(i)) for i in range(35)]
        self.tm = TM.TM(tmf.heads, tmf.terms, tmfuncs, self.table, tmf.read)
        tmf.attach(self.tm)

    def run(self, prog):
        self.lex = self.fsm.run(prog)
        self.pol = self.tm.run(self.lex)
        #print(self.pol)
        pfa = PFAnalyzer.PFAnalyzer(self.pol, self.table)
        pfa.analyze()
