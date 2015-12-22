"""
Program name: PIP/GPS interpreter
Module description: Functions for syntax and lexic analysers
Date: 22.12.2014
Authors:
    Grankovskiy P. A.
    Polikarpov V. N.
    Shtern A. N.
"""

class FSMfuncs:
    def __init__(self, table):
        self.ret = []
        self.table = table
        self.transtable = {
            'err': {'': ('err', 0)},
            'st': {'#': ('lbl', 2),
                   '!=': ('=', 2),
                   '/': ('/', 10),
                   '0:9': ('1', 2),
                   'A:Za:z_': ('a', 2),
                   ';+-*><(){}': ('st', 1),
                   '"': ('str', 2),
                   None: ('err', 4),
                   ' \t\n': ('st', 10),
                   '': ('err', 0)},
            'lbl': {'A:Za:z_': ('lbl', 6),
                    '': ('st', 7)},
            '=': {'=': ('st', 9),
                  '': ('st', 8)},
            '/': {'*': ('lcom', 10),
                  '/': ('com', 10),
                  '': ('err', 0)},
            '1': {'0:9': ('1', 6),
                  '': ('st', 3)},
            'a': {'A:Za:z_': ('a', 6),
                  '': ('st', 8)},
            'str': {'"': ('st', 5),
                    '\\': ('\\str', 10),
                    None: ('err', 0),
                    '': ('str', 6)},
            'lcom': {'*': ('lcom2', 10),
                     None: ('err', 0),
                     '': ('lcom', 10)},
            'com': {'\n': ('st', 10),
                    None: ('st', 10),
                    '': ('com', 10)},
            '\\str': {'"\\': ('str', 6),
                      'n': ('str', 11),
                      '': ('err', 0)},
            'lcom2': {'/': ('st', 10),
                      None: ('err', 0),
                      '': ('lcom', 10)}}
    def attach(self, fsm):
        self.fsm = fsm
    def read(self):
        self.c = self.fsm.read()
        #print(self.c, end='')
    def push(self, n):
        self.ret += [n]
    def func0(self):
        raise Exception
    def func1(self):
        self.push(self.table.num(self.c))
        self.read()
    def func2(self):
        self.cur = self.c
        self.read()
    def func3(self):
        self.table.addconst(self.cur)
        self.push(self.table.num(self.cur))
    def func4(self):
        return self.ret
    def func5(self):
        self.table.addstr(self.cur)
        self.push(self.table.num(self.cur))
        self.read()
    def func6(self):
        self.cur += self.c
        self.read()
    def func7(self):
        self.table.addlabel(self.cur)
        self.push(self.table.num(self.cur))
    def func8(self):
        self.table.addname(self.cur)
        self.push(self.table.num(self.cur))
    def func9(self):
        self.cur += self.c
        self.push(self.table.num(self.cur))
        self.read()
    def func10(self):
        self.read()
    def func11(self):
        self.cur += '\n'
        self.read()


class SynHead:
    def __init__(self, text, lst, pf):
        self.text=text
        self.lst=lst
        self.pf=pf
    def __repr__(self):
        return ' / '.join((self.text, str(self.lst), str(self.pf)))

class TMfuncs:
    def __init__(self):
        self.pfpos=0
        self.syncat=''
        self.pf=[[]]
        
        self.terms = [None,'=','+','-','*','==','>','<','!=','OR','AND','(',')','{','}','iPHONLY','ANDROIDLY','GOOGLEFOR','SMS','lbl','str','a',';'];
        self.heads = {
            ''          :[34,0,0,0,0,0,0,0,0,0,0,0,0,3,0,1,0,3,3,26,0,3,33],
            'MOP ;'     :[28,0,0,0,0,0,0,0,0,0,0,0,0,3,0,1,0,3,3,26,0,3,23],
            'lbl'       :[0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,1,0,3,3,0,0,3,25],
            '{'         :[0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,1,0,3,3,26,0,3,15],
            '{ MOP ;'   :[0,0,0,0,0,0,0,0,0,0,0,0,0,3,16,1,0,3,3,26,0,3,23],
            '{ MOP ; }' :[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,17,0,0,0,0,0,17],
            'GOOGLEFOR' :[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,13,0],
            'GOOGLEFOR a':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,0,0,0,0,0,14],
            'iPHONLY'   :[0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0],
            'iPHONLY (' :[0,0,5,5,7,5,5,5,5,9,6,3,12,0,0,0,0,0,0,0,0,3,0],
            'iPHONLY ( BE )':[0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,1,18,3,3,0,0,3,31],
            'iPHONLY ( BE ) OP ANDROIDLY':[0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,1,0,3,3,0,0,3,24],
            'str'       :[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,27,0,0,0,0,0,27],
            'a'         :[0,2,4,4,4,4,4,4,4,4,4,0,4,0,0,0,4,0,0,0,0,0,4],
            'a ='       :[0,0,5,5,7,0,0,0,0,0,0,3,0,0,0,0,21,0,0,0,0,3,21],
            'BE OR'     :[0,0,5,5,7,5,5,5,5,11,6,3,11,0,0,0,0,0,0,0,0,3,0],
            'BT AND'    :[0,0,5,5,7,5,5,5,5,10,10,3,10,0,0,0,0,0,0,0,0,3,0],
            '('         :[0,0,5,5,7,5,5,5,5,9,6,3,30,0,0,0,0,0,0,0,0,3,0],
            '( BE )'    :[0,0,0,0,0,0,0,0,0,29,29,0,29,0,0,0,0,0,0,0,0,0,0],
            'E =='      :[0,0,5,5,7,0,0,0,0,8,8,3,8,0,0,0,0,0,0,0,0,3,0],
            'E >'       :[0,0,5,5,7,0,0,0,0,8,8,3,8,0,0,0,0,0,0,0,0,3,0],
            'E <'       :[0,0,5,5,7,0,0,0,0,8,8,3,8,0,0,0,0,0,0,0,0,3,0],
            'E !='      :[0,0,5,5,7,0,0,0,0,8,8,3,8,0,0,0,0,0,0,0,0,3,0],
            'E +'       :[0,0,20,20,7,20,20,20,20,20,20,3,20,0,0,0,20,0,0,0,0,3,20],
            'E -'       :[0,0,20,20,7,20,20,20,20,20,20,3,20,0,0,0,20,0,0,0,0,3,20],
            'T *'       :[0,0,19,19,19,19,19,19,19,19,19,3,19,0,0,0,19,0,0,0,0,3,19],
            '( E )'     :[0,0,32,32,32,32,32,32,32,32,32,0,32,0,0,0,32,0,0,0,0,0,32],
            'SMS'       :[0,0,5,5,7,0,0,0,0,0,0,3,0,0,0,0,22,0,0,0,3,3,22]
        }
    
    def attach(self, tm):
        self.tm = tm
        self.stack = tm.stack
        self.stack += [SynHead('',[],None)]
        self.table = tm.table
    
    def read(self):
        self.term = self.tm.read()
        
    def error(self):
        raise Exception
    
    #---------------------------------------------
    
    def writePfLine(self,line,val):
        self.pf[line]+=[val]
        
    def writePf(self,val):
        self.writePfLine(self.pfpos,val)
    
    #---------------------------------------------
    
    def PF_POP(self):
        curh = self.stack.pop()
        for val in curh.lst:
            self.writePf(val)
    
    def PF_POP_1(self):
        curh = self.stack.pop()
        self.writePf(curh.lst[-1])
        
    def PF_POP_0(self):
        curh = self.stack.pop()
        self.writePf(curh.lst[0])
    
    def ADD_TERM(self):
        self.stack[-1].lst += [self.term]
        self.stack[-1].text += ' ' + self.table.name2(self.term)
        
    def PUSH_TERM(self):
        newh = SynHead(self.table.name2(self.term), [self.term], None)
        self.stack += [newh]
    
    #---------------------------------------------
    
    def syncase0(self):
        self.error()
        
    def syncase1(self):
        if self.syncat != '': self.error()
        
        newh = SynHead('iPHONLY', [self.table.num('iPHONLY')], self.pfpos)
        self.stack += [newh]
        
        self.read()
    
    def syncase2(self):
        if self.syncat != '': self.error()
        
        self.ADD_TERM()
        
        self.read()
        
    def syncase3(self):
        if self.syncat != '': self.error()
        
        self.PUSH_TERM()
        
        self.read()
    
    def syncase4(self):
        if self.syncat != '': self.error()
        
        self.PF_POP_1()
        
        self.syncat = 'F'
    
    def syncase5(self):
        if self.syncat not in ['F','T','E']: self.error()
        
        newh = SynHead('E '+self.table.name2(self.term), [self.term], None)
        self.stack += [newh]
        
        self.syncat = ''
        
        self.read()
        
    def syncase6(self):
        if self.syncat not in ['COM','BT']: self.error()
        
        newh = SynHead('BT AND', [self.table.num('AND')], None)
        self.stack += [newh]
        
        self.syncat = ''
        
        self.read()
        
    def syncase7(self):
        if self.syncat not in ['F','T']: self.error()
        
        newh = SynHead('T '+self.table.name2(self.term), [self.term], None)
        self.stack += [newh]
        
        self.syncat = ''
        
        self.read()
    
    def syncase8(self):
        if self.syncat not in ['F','T','E']: self.error()
        
        self.PF_POP_1()
        
        self.syncat = 'COM'
        
    def syncase9(self):
        if self.syncat not in ['COM','BT','BE']: self.error()
        
        newh = SynHead('BE OR', [self.table.num('OR')], None)
        self.stack += [newh]
        
        self.syncat = ''
        
        self.read()
        
    def syncase10(self):
        if self.syncat != 'COM': self.error()
        
        self.PF_POP_1()
        
        self.syncat = 'BT'
        
    def syncase11(self):
        if self.syncat not in ['COM','BT']: self.error()
        
        self.PF_POP_1()
        
        self.syncat = 'BE'
        
    def syncase12(self):
        if self.syncat not in ['COM','BT','BE']: self.error()
        
        self.stack[-1].lst += [self.table.num(')')]
        self.stack[-1].text += ' BE )'
        
        self.pfpos += 1
        self.pf += [[]]
        
        self.syncat = ''
        
        self.read()
        
    def syncase13(self):
        if self.syncat != '': self.error()
        
        self.ADD_TERM()
        
        self.writePf([self.term])
        
        self.read()
        
    def syncase14(self):
        if self.syncat != '': self.error()
        
        self.PF_POP_0()
        
        self.syncat = 'OP'
    
    def syncase15(self):
        if self.syncat not in ['OP','LOP','MOP']: self.error()
        
        self.stack[-1].lst += [self.table.num(';')]
        self.stack[-1].text += ' MOP ;'
        
        self.pfpos += 1
        self.pf += [[]]
        
        self.syncat = ''
        
        self.read()
    
    def syncase16(self):
        if self.syncat not in ['','OP','LOP']: self.error()
        
        self.ADD_TERM()
        
        self.syncat = ''
        
        self.read()
        
    def syncase17(self):
        if self.syncat != '': self.error()
        
        self.stack.pop()
        
        self.syncat = 'OP'
        
    def syncase18(self):
        if self.syncat != 'OP': self.error()
        
        self.writePfLine(self.stack[-1].pf, self.pfpos+1)
        self.writePfLine(self.stack[-1].pf, self.table.num('iPHONLY'))
        
        self.stack[-1].lst += [self.table.num('ANDROIDLY')]
        self.stack[-1].text += ' OP ANDROIDLY'
        
        self.stack[-1].pf = self.pfpos
        
        self.pfpos += 1
        self.pf += [[]]
        
        self.syncat = ''
        
        self.read()
        
    def syncase19(self):
        if self.syncat != 'F': self.error()
        
        self.PF_POP_1()
        
        self.syncat = 'T'
        
    def syncase20(self):
        if self.syncat not in ['F','T']: self.error()
        
        self.PF_POP_1()
        
        self.syncat = 'E'
        
    def syncase21(self):
        if self.syncat not in ['F','T','E']: self.error()
        
        self.PF_POP()
        
        self.syncat = 'OP'
        
    def syncase22(self):
        if self.syncat not in ['F','T','E','PR']: self.error()
        
        self.PF_POP_1()
        
        self.syncat = 'OP'
        
    def syncase23(self):
        if self.syncat not in ['OP','LOP']: self.error()
        
        self.pfpos += 1
        self.pf += [[]]
        
        self.syncat = ''
        
        self.read()
    
    def syncase24(self):
        if self.syncat != 'OP': self.error()
        
        self.writePfLine(self.stack[-1].pf, self.pfpos)
        self.writePfLine(self.stack[-1].pf, self.table.num('GOOGLEFOR'))
        
        self.stack.pop()
        
    def syncase25(self):
        if self.syncat != 'OP': self.error()
        
        self.stack.pop()
        
        self.syncat = 'LOP'
        
    def syncase26(self):
        if self.syncat != '': self.error()
        
        self.PUSH_TERM()
        
        self.table.setval(self.term,self.pfpos)
        
        self.read()
    
    def syncase27(self):
        if self.syncat != '': self.error()
        
        self.PF_POP_1()
        
        self.syncat = 'PR'
        
    def syncase28(self):
        if self.syncat != '': self.error()
        
        self.stack.pop()
        
        self.syncat = 'PROG'
        
    def syncase29(self):
        if self.syncat != '': self.error()
        
        self.stack.pop()
        
        self.syncat = 'COM'
        
    def syncase30(self):
        if self.syncat not in ['COM','BT','BE','F','T','E']: self.error()
        
        if self.syncat in ['COM','BT','BE']:
            self.stack[-1].lst += [self.table.num(')')]
            self.stack[-1].text += ' BE )'
        
        if self.syncat in ['F','T','E']:
            self.stack[-1].lst += [self.table.num(')')]
            self.stack[-1].text += ' E )'
        
        self.syncat = ''
        
        self.read()
        
    def syncase31(self):
        if self.syncat != 'OP': self.error()
        
        self.writePfLine(self.stack[-1].pf, self.pfpos+1)
        self.writePfLine(self.stack[-1].pf, self.table.num('iPHONLY'))
        
        self.stack.pop()
        
    def syncase32(self):
        if self.syncat != '': self.error()
        
        self.stack.pop()
        
        self.syncat = 'F'
        
    def syncase33(self):
        if self.syncat not in ['OP','LOP']: self.error()
        
        newh = SynHead('MOP '+self.table.name2(self.term), [self.term], None)
        self.stack += [newh]
        
        self.pfpos += 1
        self.pf += [[]]
        
        self.syncat = ''
        
        self.read()
    
    def syncase34(self):
        if self.syncat != 'PROG': self.error()
        
        for i,val in enumerate(self.pf):
            if val and type(val[0]) == list:
                res = self.table.labelval(val[0][0])
                if res == None:
                    self.error();
                else:
                    self.pf[i][0] = res
        
        return self.pf
        
