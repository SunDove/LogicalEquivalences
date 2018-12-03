########################
#   Abstract classes   #
########################

class Expr:
    def __init__(self):
        pass

    def getChild(self):
        pass

    def __str__(self):
        pass

    def __eq__(self, other):
        return self.__str__() == str(other)

    def replace(self, exp1, exp2):
        if self==exp1:
            return exp2
        else:
            if isinstance(self, BinaryOp):
                return type(self)(self.getFirstChild().replace(exp1, exp2), self.getSecondChild().replace(exp1, exp2))
            elif isinstance(self, UnaryOp):
                return type(self)(self.getChild().replace(exp1, exp2))
            else:
                return self

class Const(Expr):
    def __init__(self, e):
        pass

    def getValue(self):
        pass

    def getChild(self):
        return None


class BinaryOp(Expr):
    def __init__(self, e1, e2):
        if isinstance(e1, Expr) and isinstance(e2, Expr):
            self.child1 = e1
            self.child2 = e2
        else:
            raise ValueError("Invalid argument for BinaryOp constructor")

    def getFirstChild(self):
        return self.child1

    def getSecondChild(self):
        return self.child2

    def getChild(self):
        return [self.child1, self.child2]

    def setChild(self, e1, e2):
        self.child1 = e1
        self.child2 = e2

    def setFirstChild(self, e1):
        self.child1 = e1

    def setSecondChild(self, e2):
        self.child2 = e2

# This might not be necessary but whatever
class UnaryOp(Expr):
    def __init__(self, e):
        if isinstance(e, Expr):
            self.child = e
        else:
            raise ValueError("Invalid argument for Unary constructor")

    def getChild(self):
        return self.child

    def setChild(self, e):
        self.child = e

########################
#   Concrete classes   #
########################


class Bool(Const):
    def __init__(self, b):
        if isinstance(b, bool):
            self.value = b
        else:
            raise ValueError("Invalid argumet for Bool constructor")

    def __str__(self):
        return "Bool(" + str(self.value) + ")"

    def __eq__(self, other):
        return self.__str__() == str(other)

class Var(Const):
    def __init__(self, s):
        if isinstance(s, str):
            self.value = s
        else:
            raise ValueError("Invalid argument for Var constructor")

    def __str__(self):
        return "Var(" + str(self.value) + ")"

    def __eq__(self, other):
        return self.__str__() == str(other)

class Not(UnaryOp):
    def __str__(self):
        return "Not(" + str(self.getChild()) + ")"

class And(BinaryOp):
    def __str__(self):
        return "And(" + str(self.getFirstChild()) + ", " + str(self.getSecondChild()) + ")"

class Or(BinaryOp):
    def __str__(self):
        return "Or(" + str(self.getFirstChild()) + ", " + str(self.getSecondChild()) + ")"

class Xor(BinaryOp):
    def __str__(self):
        return "Xor(" + str(self.getFirstChild()) + ", " + str(self.getSecondChild()) + ")"

class Cond(BinaryOp):
    def __str__(self):
        return "Cond(" + str(self.getFirstChild()) + ", " + str(self.getSecondChild()) + ")"

class BiCond(BinaryOp):
    def __str__(self):
        return "BiCond(" + str(self.getFirstChild()) + ", " + str(self.getSecondChild()) + ")"
