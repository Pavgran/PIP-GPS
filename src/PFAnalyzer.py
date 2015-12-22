"""
Program name: PIP/GPS interpreter
Module description: Poland form interpreter
Date: 22.12.2014
Authors:
    Grankovskiy P. A.
    Polikarpov V. N.
    Shtern A. N.
"""

class StackItem:
    def __init__(self,num,type):
        self.num=num
        self.type=type

class PFAnalyzer:
    def __init__(self, pf,table):
        self.pf = pf
        self.table=table
        self.i=0
        self.j=0
        self.stack=[]
        
    def oper_plus(self):
        b=self.stack.pop()
        a=self.stack.pop()
        type_b = b.type
        type_a = a.type
        if type_a != 'value': 
            a=self.table.val(a.num) 
        else:
            a = a.num
        if type_b != 'value': 
            b=self.table.val(b.num) 
        else: 
            b = b.num   
        self.stack.append(StackItem(a+b,'value'))
    
    def oper_minus(self):
        b=self.stack.pop()
        a=self.stack.pop()
        type_b = b.type
        type_a = a.type
        if type_a != 'value': 
            a=self.table.val(a.num) 
        else:
            a = a.num
        if type_b != 'value': 
            b=self.table.val(b.num) 
        else: 
            b = b.num   
        
        self.stack.append(StackItem(a-b,'value'))
        
    def oper_multiply(self):
        b=self.stack.pop()
        a=self.stack.pop()
        type_b = b.type
        type_a = a.type
        
        if type_a != 'value': 
            a=self.table.val(a.num) 
        else: 
            a = a.num
            
        if type_b != 'value': 
            b=self.table.val(b.num) 
        else: 
            b = b.num   
        self.stack.append(StackItem(a*b,'value'))
    
    def oper_equals(self):
        b=self.stack.pop()
        a=self.stack.pop()
        type_b = b.type
        type_a = a.type
        if type_a != 'value': 
            a=self.table.val(a.num) 
        else: 
            a = a.num
        if type_b != 'value': 
            b=self.table.val(b.num) 
        else:
            b = b.num   
        if a==b: 
            self.stack.append(StackItem(True,'value'))
        else: 
            self.stack.append (StackItem(False,'value'))
        
    def oper_not_equals(self):
        b=self.stack.pop()
        a=self.stack.pop()
        type_b = b.type
        type_a = a.type
        if type_a != 'value': 
            a=self.table.val(a.num) 
        else: 
            a = a.num
            
        if type_b != 'value': 
            b=self.table.val(b.num) 
        else: 
            b = b.num
            
        if a!=b: 
            self.stack.append(StackItem(True,'value'))
        else: 
            self.stack.append (StackItem(False,'value'))
        
    def oper_bigger(self):
        b=self.stack.pop()
        a=self.stack.pop()
        type_b = b.type
        type_a = a.type
        if type_a != 'value': 
            a=self.table.val(a.num) 
        else:
            a = a.num
        if type_b != 'value': 
            b=self.table.val(b.num) 
        else: 
            b = b.num
            
        if a>b:
            self.stack.append(StackItem(True,'value'))
        else:
            self.stack.append(StackItem(False,'value'))
    
    def oper_smaller(self):
        b=self.stack.pop()
        a=self.stack.pop()
        type_b = b.type
        type_a = a.type
        if type_a != 'value': 
            a=self.table.val(a.num) 
        else:
            a = a.num
        if type_b != 'value':
            b=self.table.val(b.num) 
        else:
            b = b.num   
        if a<b:
            self.stack.append(StackItem(True,'value'))
        else:
            self.stack.append(StackItem(False,'value'))
        
    def oper_or(self):
        b=self.stack.pop()
        a=self.stack.pop()
        type_b = b.type
        type_a = a.type
        if type_a != 'value':
            a=self.table.val(a.num) 
        else:
            a = a.num
            
        if type_b != 'value':
            b=self.table.val(b.num) 
        else:
            b = b.num   
            self.stack.append (StackItem(a or b,'value'))

    def oper_and(self):
        b=self.stack.pop()
        a=self.stack.pop()
        type_b = b.type
        type_a = a.type
        if type_a != 'value':
            a=self.table.val(a.num) 
        else:
            a = a.num
        if type_b != 'value':
            b=self.table.val(b.num) 
        else:
            b = b.num   
            self.stack.append (StackItem(a and b,'value'))
        
    def oper_ass(self):
        var=self.stack.pop()
        value=self.stack.pop()
        type_var = var.type;
        type_val = value.type;
        if type_val != 'value':
            value = self.table.val(value.num) 
        else:
            value = value.num
        if type_var == 'value':
            print('FATAL ERROR') 
        else:
            self.table.setval(var.num,value)
    
    def oper_iphonly(self):
        b=self.stack.pop()
        a=self.stack.pop()

        type_a = a.type
        if type_a != 'value':
            a=self.table.val(a.num) 
        else:
            a = a.num
 
        if a == False:
            self.i=b.num
        else:
            self.i=self.i+1
            
        self.j=-1
        self.stack=[]
        
    def oper_googlefor(self):
        a=self.stack.pop()

        
        self.i=a.num
        self.j=-1
        self.stack=[]
        
    def oper_SMS(self):
        a=self.stack.pop()
        type=a.type
        if type != 'value':
            a=self.table.val(a.num) 
        else:
            a = a.num
        print(a, end='')
        
    def analyze(self):
        funcs= {'+':self.oper_plus,'-':self.oper_minus,'*':self.oper_multiply,'==':self.oper_equals,'!=':self.oper_not_equals,'>':self.oper_bigger,'<':self.oper_smaller,'OR':self.oper_or,'AND':self.oper_and,'=':self.oper_ass,'iPHONLY':self.oper_iphonly,'GOOGLEFOR': self.oper_googlefor,'SMS':self.oper_SMS}
        end = False
        self.i=0
        self.j=0
        while not end:
            if self.pf[self.i]: 
                curr = self.pf[self.i][self.j]
                if curr>=0:
                    self.stack.append(StackItem(curr,'num'))
                else:
                    funcs[self.table.name(curr)]()
            self.j=self.j+1
            if self.j>=len(self.pf[self.i]):
                self.j=0
                self.i=self.i+1
                self.stack=[]
                
            if self.i == len(self.pf):
                end = True
            
    
    
    
        
    