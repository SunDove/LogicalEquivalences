import unittest
from AST import *
from parser import Parser

class TestAST(unittest.TestCase):

    def setUp(self):
        self.boolTrue = Bool(True)
        self.boolFalse = Bool(False)
        self.notTrue = Not(self.boolTrue)

    def testEq(self):
        # Bool
        self.assertEqual(Bool(True), Bool(True))
        self.assertNotEqual(self.boolFalse, self.boolTrue)

        # Var
        self.assertEqual(Var("a"), Var("a"))
        self.assertNotEqual(Var("a"), Var("b"))

        # Not
        self.assertEqual(Not(self.boolTrue), Not(self.boolTrue))
        self.assertNotEqual(Not(self.boolFalse), Not(self.boolTrue))

        binOps = [And, Or, Xor, Cond, BiCond]

        for op in binOps:
            self.assertEqual(op(self.boolTrue, self.boolTrue), op(self.boolTrue, self.boolTrue))
            self.assertNotEqual(op(self.boolFalse, self.boolFalse), op(self.boolFalse, self.boolTrue))
            self.assertNotEqual(op(self.boolFalse, self.boolFalse), op(self.boolTrue, self.boolFalse))

    def testConstructors(self):
        self.assertRaises(ValueError, Bool, self.boolTrue)
        self.assertRaises(ValueError, Var, self.boolTrue)

        self.assertRaises(ValueError, lambda: Not(True))

        binOps = [And, Or, Xor, Cond, BiCond]

        for op in binOps:
            self.assertRaises(ValueError, op, True, True)
            self.assertRaises(ValueError, op, self.boolFalse, True)

    def testParser(self):
        p = Parser()
        self.assertEqual(p.parse('p'), Var('p'))
        self.assertEqual(p.parse('T'), self.boolTrue)
        self.assertEqual(p.parse('p^q'), And(Var('p'), Var('q')))
        self.assertEqual(p.parse('(pvq)->r'), Cond(Or(Var('p'), Var('q')), Var('r')))

        self.assertRaises(Exception, p.parse, '(p^q')
        self.assertRaises(Exception, p.parse, '(p)q(r)')

if __name__ == "__main__":
    unittest.main()
