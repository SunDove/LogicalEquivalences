import re
import time

from AST import *

class Parser:

    def __init__(self):
        self.operators = ['~', '^', 'v', 'x', '->', '[=]'] #[Not, And, Or, Xor, Conditional, BiConditional]

    def parse(self, str):
        print(str)
        str = str.replace(' ', '')
        if str.count('(')!=str.count(')'):
            raise Exception('Unequal number of opening and closing parentheses in expression')
        while str[0]=='(' and str[-1]==')' and str.find(')') == len(str)-1 and str.rfind('(')==0:
            str = str[1:-1]
        if str.count('(')==0:
            #Base case
            occ = [str.count(o) for o in self.operators]
            if sum(occ[1:]) > 1:
                raise Exception('Only one operator is allowed per set of parentheses')
            if sum(occ[1:]) < 1:
                if occ[0]==0:
                    if str=='T':
                        return Bool(True)
                    if str=='F':
                        return Bool(False)
                    return Var(str)
                else:
                    return Not(self.parse(str[1:]))
            if sum(occ[1:])==1:
                oper = ''
                for i in range(1, len(occ)):
                    o = occ[i]
                    if o==1:
                        oper = self.operators[i]
                        break
                ind = str.index(oper)
                p1 = self.parse(str[:ind])
                p2 = self.parse(str[ind+len(oper):])
                if oper=='^':
                    return And(p1, p2)
                if oper=='v':
                    return Or(p1, p2)
                if oper=='x':
                    return Xor(p1, p2)
                if oper=='->':
                    return Cond(p1, p2)
                if oper=='[=]':
                    return BiCond(p1, p2)
        else:
            close = str.find(')')
            open = str.rfind('(')
            if open < close:
                mid = self.parse(str[open+1:close])
                temp = '%.20f' % time.time()
                p = self.parse(str[:open] + temp + str[close+1:])
                return p.replace(Var(temp), mid)
            else:
                p2 = None
                opInd = -1
                oper = ''
                if str[0]=='(':
                    opInd = close+1
                    for o in self.operators[1:]:
                        if str[opInd:opInd+len(o)]==o:
                            oper = o
                            break
                    if oper=='':
                        raise Exception('Invalid operation')
                else:
                    opInd, op = min([(str.find(o), oper) for o in self.operators[1:]])
                p1 = self.parse(str[0:opInd])
                p2 = self.parse(str[opInd+len(oper):])
                if oper=='^':
                    return And(p1, p2)
                if oper=='v':
                    return Or(p1, p2)
                if oper=='x':
                    return Xor(p1, p2)
                if oper=='->':
                    return Cond(p1, p2)
                if oper=='[=]':
                    return BiCond(p1, p2)
