import re
import time

class Parser:

    def __init__(self):
        self.operators = ['~', '^', 'v', '->', '[=]'] #[Not, And, Or, Conditional, BiConditional]

    def parse(self, str):
        str = str.replace(' ', '')
        if str.count('(')!=str.count(')'):
            raise Exception('Unequal number of opening and closing parentheses in expression')
        try:
            while str[0]=='(' and str[-1]==')':
                str = str[1:-1]
        except IndexError:
            print(str)
        if str.count('(')==0:
            #Base case
            occ = [str.count(o) for o in self.operators]
            if sum(occ[1:]) > 1:
                raise Exception('Only one operator is allowed per set of parentheses')
            if sum(occ[1:]) < 1:
                ret = ''
                for i in range(occ[0]):
                    ret += 'Not('
                val = str.replace(self.operators[0], '')
                if val=='T':
                    val = True
                if val=='F':
                    val = False
                ret += 'Const(%s)' % val
                for i in range(occ[0]):
                    ret += ')'
                return ret
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
                return 'Oper(%s, %s)' % (p1, p2)
        else:
            close = str.find(')')
            open = str.rfind('(')
            mid = self.parse(str[open+1:close])
            temp = '%.20f' % time.time()
            p = self.parse(str[:open] + temp + str[close+1:])
            return p.replace('Const(%s)'%temp, mid)
