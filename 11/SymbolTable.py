class SymbolTable:

    class_table = None
    subroutine_table = None
    var_count = None

    def __init__(self):
        self.class_table = {}
        self.subroutine_table = {}
        self.var_count = {'static':0,'this':0,'argument':0,'local':0}
        
    def startSubroutine(self):
        self.subroutine_table = {}
        self.var_count['local']=0
        self.var_count['argument']=0
        
    def define(self,name,type,kind):
        '''.'''
        if kind in ('static','field'):
            if kind == 'field':
                kind = 'this'
            self.class_table[name] = (type,kind,self.varCount(kind))
            self.var_count[kind] += 1
        elif kind in ('argument','var'):
            if kind == 'var':
                kind = 'local'
            self.subroutine_table[name] = (type,kind,self.varCount(kind))
            self.var_count[kind] += 1


    def refactor(self):
        res = {}
        for i, item in enumerate(self.subroutine_table):
            if self.subroutine_table[item][1] == 'argument':
                res[item] = (self.subroutine_table[item][0], self.subroutine_table[item][1], self.subroutine_table[item][2]+1)  
            else:
                res[item] = self.subroutine_table[item]

        self.var_count['argument'] += 1
        self.subroutine_table = res

    def varCount(self,kind):
        '''.'''
        if kind in self.var_count:
            return self.var_count[kind]

        
    def kindOf(self,name):  
        '''.'''
        if name in self.subroutine_table:
            return self.subroutine_table[name][1]
        elif name in self.class_table:
            return self.class_table[name][1]
        
    def typeOf(self,name):
        '''.'''
        if name in self.subroutine_table:
            return self.subroutine_table[name][0]
        elif name in self.class_table:
            return self.class_table[name][0]
        
    def indexOf(self,name):
        '''.'''
        if name in self.subroutine_table:
            return self.subroutine_table[name][2]
        elif name in self.class_table:
            return self.class_table[name][2]