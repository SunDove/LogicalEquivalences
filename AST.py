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

    def getNeighbors(self):
        neighbors = []
        if isinstance(self, Bool):
            return neighbors
        if isinstance(self, Not):
            count = 1
            n = self
            while isinstance(n.getChild(), Not):
                n = n.getChild()
                count+=1
                if count >= 4:
                    return neighbors
        neighbors.append(Not(Not(self)))

        return neighbors


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

    def getNeighbors(self):
        neighbors = []
        c1n = self.child1.getNeighbors()
        for c in c1n:
            neighbors.append(type(self)(c, self.child2))
        c2n = self.child2.getNeighbors()
        for c in c2n:
            neighbors.append(type(self)(self.child1, c))

        return neighbors + super().getNeighbors()

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

    def getNeighbors(self):
        neighbors = []
        cn = self.child.getNeighbors()
        for c in cn:
            addn = True
            if isinstance(c, Not):
                count = 2
                n = c.getChild()
                while isinstance(n, Not):
                    n = c.getChild()
                    count+=1
                    if count >= 4:
                        addn = False
                        break
            if addn:
                neighbors.append(type(self)(c))

        return neighbors + super().getNeighbors()

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

    def getNeighbors(self):
        c = self.getChild()
        neighbors = []
        if isinstance(c, Bool): #simplify not(bool) to just not bool
            neighbors.append(Bool(not c.value))

        #DeMorgan's Laws:
        if isinstance(c, And):
            a = c
            neighbors.append(Or(Not(a.getFirstChild()), Not(a.getSecondChild())))
        if isinstance(c, Or):
            a = c
            neighbors.append(And(Not(a.getFirstChild()), Not(a.getSecondChild())))

        #Double negation law
        if isinstance(c, Not):
            neighbors.append(c.child)

        if isinstance(c, Cond):
            neighbors.append(And(c.getFirstChild(), Not(c.getSecondChild())))

        if isinstance(c, BiCond):
            neighbors.append(BiCond(c.getFirstChild(), Not(c.getSecondChild())))

        return neighbors + super().getNeighbors()

class And(BinaryOp):
    def __str__(self):
        return "And(" + str(self.getFirstChild()) + ", " + str(self.getSecondChild()) + ")"

    def getNeighbors(self):
        c1 = self.getFirstChild()
        c2 = self.getSecondChild()
        neighbors = []

        # Identity law
        if c2 == Bool(True):
            neighbors.append(c1)
        if c1 == Bool(True):
            neighbors.append(c2)

        # Domination law
        if c1 == Bool(False) or c2 == Bool(False):
            neighbors.append(Bool(False))

        # Idempotent laws
        if c1 == c2:
            neighbors.append(c1)

        # Commutative law
        # Potential cycle here :/
        neighbors.append(And(c2, c1))

        # Associative law
        # Potential cycle here too ;/
        if isinstance(c1, And):
            neighbors.append(And(c1.getFirstChild(), And(c1.getSecondChild(), c2)))

        # Distributive law
        if isinstance(c2, Or):
            neighbors.append(Or(And(c1, c2.getFirstChild()), And(c1, c2.getSecondChild())))
        if isinstance(c1, Or):
            neighbors.append(Or(And(c2, c1.getFirstChild()), And(c2, c1.getSecondChild())))

        # De Morgan's law
        neighbors.append(Not(Or(c1, c2)))

        # Absorption law
        if isinstance(c2, Or) and (c1 in c2.getChild()):
            neighbors.append(c1)
        if isinstance(c1, Or) and (c2 in c1.getChild()):
            neighbors.append(c2)

        # Negation law
        if isinstance(c2, Not) and c1 == c2.getChild():
            neighbors.append(Bool(False))
        if isinstance(c1, Not) and c2 == c1.getChild():
            neighbors.append(Bool(False))

        # 7.4
        neighbors.append(Not(Cond(c1, Not(c2))))

        # 7.6
        if isinstance(c1, Cond) and isinstance(c2, Cond) and c1.getFirstChild() == c2.getFirstChild():
            neighbors.append(Cond(c1.getFirstChild(), And(c1.getSecondChild(), c2.getSecondChild())))

        # 7.7
        if isinstance(c1, Cond) and isinstance(c2, Cond) and c1.getSecondChild() == c2.getSecondChild():
            neighbors.append(Cond(Or(c1.getFirstChild(), c2.getSecondChild()), c1.getSecondChild()))

        return neighbors + super().getNeighbors()

class Or(BinaryOp):
    def __str__(self):
        return "Or(" + str(self.getFirstChild()) + ", " + str(self.getSecondChild()) + ")"

    def getNeighbors(self):
        c1 = self.getFirstChild()
        c2 = self.getSecondChild()
        neighbors = []

        # Identity law
        if c2 == Bool(False):
            neighbors.append(c1)
        if c1 == Bool(False):
            neighbors.append(c2)

        # Domination law
        if c2 == Bool(True) or c1 == Bool(True):
            neighbors.append(Bool(True))

        # Idempotent law
        if c1 == c2:
            neighbors.append(c1)

        # Commutative law
        neighbors.append(Or(c2, c1))

        # Associative law
        if isinstance(c1, Or):
            neighbors.append(Or(c1.getFirstChild(), Or(c1.getSecondChild(), c2)))

        # Distributive law
        if isinstance(c2, And):
            neighbors.append(And(Or(c1, c2.getFirstChild()), Or(c1, c2.getSecondChild())))
        if isinstance(c1, And):
            neighbors.append(And(Or(c2, c1.getFirstChild()), Or(c2, c1.getSecondChild())))

        # De Morgan's law
        neighbors.append(Not(And(c1, c2)))

        # Absorption law
        if isinstance(c2, And) and (c1 in c2.getChild()):
            neighbors.append(c1)
        if isinstance(c1, And) and (c2 in c1.getChild()):
            neighbors.append(c2)

        # Negation law
        if isinstance(c2, Not) and c1 == c2.getChild():
            neighbors.append(Bool(True))
        if isinstance(c1, Not) and c2 == c1.getChild():
            neighbors.append(Bool(True))

        # 7.3
        neighbors.append(Cond(Not(c1), c2))

        # 7.8
        if (isinstance(c1, Cond) and isinstance(c2, Cond)
            and c1.getFirstChild() == c2.getFirstChild()):
            neighbors.append(Cond(c1.getFirstChild(), Or(c1.getSecondChild(), c2.getSecondChild())))

        # 7.9
        if (isinstance(c1, Cond) and isinstance(c2, Cond)
            and c1.getSecondChild() == c2.getSecondChild()):
            neighbors.append(Cond(And(c1.getFirstChild(), c2.getFirstChild()), c1.getSecondChild()))

        return neighbors + super().getNeighbors()


class Xor(BinaryOp):
    def __str__(self):
        return "Xor(" + str(self.getFirstChild()) + ", " + str(self.getSecondChild()) + ")"

class Cond(BinaryOp):
    def __str__(self):
        return "Cond(" + str(self.getFirstChild()) + ", " + str(self.getSecondChild()) + ")"

    def getNeighbors(self):
        c1 = self.getFirstChild()
        c2 = self.getSecondChild()
        neighbors = []

        # 7.1
        neighbors.append(Or(Not(c1), c2))

        # 7.2
        neighbors.append(Cond(Not(c2), Not(c1)))

        return neighbors + super().getNeighbors()

class BiCond(BinaryOp):
    def __str__(self):
        return "BiCond(" + str(self.getFirstChild()) + ", " + str(self.getSecondChild()) + ")"

    def getNeighbors(self):
        c1 = self.getFirstChild()
        c2 = self.getSecondChild()
        neighbors = []

        # 8.1
        neighbors.append(And(Cond(c1, c2), Cond(c2, c1)))

        # 8.2
        neighbors.append(BiCond(Not(c1), Not(c2)))

        # 8.3
        neighbors.append(Or(And(c1, c2), And(Not(c1), Not(c2))))

        return neighbors + super().getNeighbors()
