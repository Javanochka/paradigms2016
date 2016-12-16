import unittest
from io import StringIO
from unittest.mock import patch
from operator import *
from model import *


class ScopeTest(unittest.TestCase):
    def test_one_in_current_scope(self):
        scope = Scope()
        scope['a'] = 24
        self.assertEqual(scope['a'], 24)

    def test_many_in_current_scope(self):
        scope = Scope()
        scope['a'] = 24
        scope['A'] = 27
        self.assertEqual(scope['a'], 24)
        self.assertEqual(scope['A'], 27)

    def test_in_parent_scope(self):
        par = Scope()
        par['a'] = 24
        scope = Scope(par)
        self.assertEqual(scope['a'], 24)

    def test_multiple_def(self):
        par = Scope()
        par['a'] = 24
        scope = Scope(par)
        scope['a'] = 42
        self.assertEqual(scope['a'], 42)


class NumberTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()

    def test_evaluate(self):
        num = Number(243)
        self.assertIsInstance(num.evaluate(self.scope), Number)
        self.assertIs(num.evaluate(self.scope), num)


class FunctionTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()

    def test_evaluate_not_empty(self):
        num = Number(42)
        fun = Function([], [Number(1), Number(3), Number(4), num])
        self.assertIs(fun.evaluate(self.scope), num)

    def test_evaluate_empty(self):
        '''It just shouldn't break down '''
        fun = Function([], [])
        fun.evaluate(self.scope)


class FunctionDefinitionTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()

    def test_evaluate(self):
        fun = Function([], [Number(1), Number(3), Number(4)])
        fun_def = FunctionDefinition("blabla", fun)
        fun1 = fun_def.evaluate(self.scope)
        self.assertIs(self.scope["blabla"], fun)
        self.assertIs(fun1, fun)


class ConditionalTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()
        self.scope["a"] = Number(1)
        self.scope["b"] = Number(0)
        self.scope["c"] = Number(239)

    def test_iftrue_1_both_not_empty(self):
        cond = Conditional(self.scope["a"], [self.scope["a"], self.scope["b"]], [self.scope["c"]])
        self.assertIs(cond.evaluate(self.scope), self.scope["b"])

    def test_iftrue_239_both_not_empty(self):
        cond = Conditional(self.scope["c"], [self.scope["a"], self.scope["b"]], [self.scope["c"]])
        self.assertIs(cond.evaluate(self.scope), self.scope["b"])

    def test_iffalse_both_not_empty(self):
        cond = Conditional(self.scope["b"], [self.scope["a"], self.scope["b"]], [self.scope["c"]])
        self.assertIs(cond.evaluate(self.scope), self.scope["c"])

    def test_iftrue_iftrue_is_empty(self):
        cond = Conditional(self.scope["a"], [], [self.scope["c"]])
        cond.evaluate(self.scope)

    def test_iffalse_iffalse_is_empty(self):
        cond = Conditional(self.scope["b"], [])
        cond.evaluate(self.scope)

    def test_iffalse_iffalse_is_none(self):
        cond = Conditional(self.scope["b"], None)
        cond.evaluate(self.scope)


class PrintTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()
        self.scope['a'] = Number(43)
        self.scope['b'] = Number(56)
        self.scope['c'] = Number(-348)
        self.scope['d'] = Number(0)

    def test_evaluate_different_numbers(self):
        with patch("sys.stdout", new_callable=StringIO) as mocked_out:
            Print(self.scope['a']).evaluate(self.scope)
            self.assertEqual(mocked_out.getvalue(), '43\n')
            Print(self.scope['b']).evaluate(self.scope)
            self.assertEqual(mocked_out.getvalue(), '43\n56\n')
            Print(self.scope['c']).evaluate(self.scope)
            self.assertEqual(mocked_out.getvalue(), '43\n56\n-348\n')
            Print(self.scope['d']).evaluate(self.scope)
            self.assertEqual(mocked_out.getvalue(), '43\n56\n-348\n0\n')


class ReadTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()

    def test_evaluate_different_numbers(self):
        for i in range(-5, 5):
            with self.subTest(i=i):
                with patch("sys.stdin", StringIO(str(i)+"\n")), patch("sys.stdout", new_callable=StringIO) as mocked_out:
                    Read("a").evaluate(self.scope)
                    Print(self.scope["a"]).evaluate(self.scope)
                    self.assertEqual(mocked_out.getvalue(), str(i)+"\n")


class ReferenceTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()
        self.scope["num"] = Number(0)
        self.scope["a"] = Number(43)
        self.scope["b"] = Number(-24)

    def test_evaluate(self):
        ref = Reference("num")
        self.assertIs(ref.evaluate(self.scope), self.scope["num"])
        ref = Reference("a")
        self.assertIs(ref.evaluate(self.scope), self.scope["a"])
        ref = Reference("b")
        self.assertIs(ref.evaluate(self.scope), self.scope["b"])


class FunctionCallTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()
        self.scope["magic"] = Number(566)
        self.patcher = patch("sys.stdout", new_callable=StringIO)
        self.mocked_out = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_nothing_is_empty_answer_is_arg(self):
        fun = Function(['a', 'b', 'c'], [Number(0), Reference('b')])
        fun_def = FunctionDefinition("fun", fun)
        fun_call = FunctionCall(fun_def, [Number(1), Number(2), Number(3)])
        Print(fun_call.evaluate(self.scope)).evaluate(self.scope)
        self.assertEqual(self.mocked_out.getvalue(), '2\n')

    def test_nothing_is_empty_answer_is_const(self):
        fun = Function(['a', 'b', 'c'], [Reference('b'), Number(239)])
        fun_def = FunctionDefinition("fun", fun)
        fun_call = FunctionCall(fun_def, [Number(1), Number(2), Number(3)])
        Print(fun_call.evaluate(self.scope)).evaluate(self.scope)
        self.assertEqual(self.mocked_out.getvalue(), '239\n')

    def test_nothing_is_empty_answer_is_global(self):
        fun = Function(['a', 'b', 'c'], [Number(0), Reference('b'), Reference('magic')])
        fun_def = FunctionDefinition("fun", fun)
        fun_call = FunctionCall(fun_def, [Number(1), Number(2), Number(3)])
        Print(fun_call.evaluate(self.scope)).evaluate(self.scope)
        self.assertEqual(self.mocked_out.getvalue(), '566\n')

    def test_nothing_is_empty_multidef(self):
        fun = Function(['a', 'b', 'magic'], [Number(0), Reference('b'), Reference('magic')])
        fun_def = FunctionDefinition("fun", fun)
        fun_call = FunctionCall(fun_def, [Number(1), Number(2), Number(3)])
        Print(fun_call.evaluate(self.scope)).evaluate(self.scope)
        self.assertEqual(self.mocked_out.getvalue(), '3\n')

    def test_without_args_answer_is_global(self):
        fun = Function([], [Number(0), Number(34), Reference('magic')])
        fun_def = FunctionDefinition("fun", fun)
        fun_call = FunctionCall(fun_def, [])
        Print(fun_call.evaluate(self.scope)).evaluate(self.scope)
        self.assertEqual(self.mocked_out.getvalue(), '566\n')

    def test_without_args_answer_is_const(self):
        fun = Function([], [Number(0), Number(34)])
        fun_def = FunctionDefinition("fun", fun)
        fun_call = FunctionCall(fun_def, [])
        Print(fun_call.evaluate(self.scope)).evaluate(self.scope)
        self.assertEqual(self.mocked_out.getvalue(), '34\n')


class BinaryOperationTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()
        self.ar_ops = {
            '+': add,
            '-': sub,
            '*': mul,
            '/': floordiv,
            '%': mod
        }
        self.lo_ops = {
            '==': eq,
            '!=': ne,
            '<': lt,
            '>': gt,
            '<=': le,
            '>=': ge,
            '&&': lambda x,y: 1 if x != 0 and y != 0 else 0,
            '||': lambda x,y: 1 if x != 0 or y != 0 else 0
        }

    def test_arithmetic(self):
        for i in range(-5, 5):
            for j in range(-5, 5):
                for op, fun in self.ar_ops.items():
                    triple = (i,j,op)
                    if j == 0 and (op == '/' or op == '%'):
                        continue
                    with self.subTest(triple = triple):
                        with patch("sys.stdout", new_callable=StringIO) as mocked_out:
                            self.scope['a'] = Number(i)
                            self.scope['b'] = Number(j)
                            Print(BinaryOperation(self.scope['a'], op, self.scope['b']).evaluate(self.scope)).evaluate(self.scope)
                            self.assertEqual(mocked_out.getvalue(), str(fun(i,j)) + '\n')

    def test_logic(self):
        for i in range(-5, 5):
            for j in range(-5, 5):
                for op, fun in self.lo_ops.items():
                    triple = (i,j,op)
                    with self.subTest(triple = triple):
                        with patch("sys.stdout", new_callable=StringIO) as mocked_out:
                            self.scope['a'] = Number(i)
                            self.scope['b'] = Number(j)
                            Print(BinaryOperation(self.scope['a'], op, self.scope['b']).evaluate(self.scope)).evaluate(self.scope)
                            if fun(i,j):
                                self.assertNotEqual(mocked_out.getvalue(), '0\n')
                            else:
                                self.assertEqual(mocked_out.getvalue(), '0\n')


class UnaryOperationTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()
    
    def test_neg(self):
        for i in range(-5, 5):
            with self.subTest(i = i):
                with patch("sys.stdout", new_callable=StringIO) as mocked_out:
                    self.scope['a'] = Number(i)
                    Print(UnaryOperation('-', self.scope['a']).evaluate(self.scope)).evaluate(self.scope)
                    self.assertEqual(mocked_out.getvalue(), str(-i) + '\n')

    def test_not(self):
        for i in range(-5, 5):
            with self.subTest(i = i):
                with patch("sys.stdout", new_callable=StringIO) as mocked_out:
                    self.scope['a'] = Number(i)
                    Print(UnaryOperation('!', self.scope['a']).evaluate(self.scope)).evaluate(self.scope)
                    if not i:
                        self.assertNotEqual(mocked_out.getvalue(), '0\n')
                    else:
                        self.assertEqual(mocked_out.getvalue(), '0\n')


if __name__ == '__main__':
    unittest.main()
