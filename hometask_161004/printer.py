from model import *

class PrettyPrinter:
    def __init__(self):
        self.visitor = PrinterVisitor()
    
    def visit(self, tree):
        tree.accept(self.visitor)


class PlainPrinter:
    def __init__(self):
        pass

    def visitNumber(self, num):
        return str(num.value)

    def visitReference(self, ref):
        return ref.name

    def visitBinaryOperation(self, bin_op):
        return ("({0} {1} {2})".format(bin_op.lhs.accept(self), bin_op.op, bin_op.rhs.accept(self)))

    def visitUnaryOperation(self, un_op):
        return ("({0}{1})".format(un_op.op, un_op.expr.accept(self)))

    def visitFunctionCall(self, fun_call):
        return "{0}({1})".format(fun_call.fun_expr.accept(self), ", ".join([expr.accept(self) for expr in fun_call.args]))


class PrinterVisitor:
    def __init__(self):
        self.spaces = 0
        self.plain = PlainPrinter()

    def visitConditional(self, conditional):
        print(" " * self.spaces + "if ({0}) ".format(conditional.condition.accept(self.plain)) + "{")
        self.spaces += 4
        for expr in conditional.if_true:
            expr.accept(self)
        self.spaces -= 4
        if conditional.if_false == None:
            print("};")
        else:
            print(" " * self.spaces + "} else {")
            self.spaces += 4
            for expr in conditional.if_false:
                expr.accept(self)
            self.spaces -= 4
            print(" " * self.spaces + "};")
        
    def visitFunctionDefinition(self, fun_def):
        print(" " * self.spaces + "def {0}({1}) ".format(fun_def.name, ", ".join(fun_def.function.args)) + "{")
        self.spaces += 4
        for expr in fun_def.function.body:
            expr.accept(self)
        self.spaces -= 4
        print(" " * self.spaces + "};")

    def visitPrint(self, print_s):
        print(" " * self.spaces + "print {0};".format(print_s.expr.accept(self.plain)))

    def visitRead(self, read_s):
        print(" " * self.spaces + "read {0};".format(read_s.name))

    def visitNumber(self, num):
        print(" " * self.spaces + "{0};".format(num.value))

    def visitReference(self, ref):
        print(" " * self.spaces + "{0};".format(ref.name))

    def visitBinaryOperation(self, bin_op):
        print(" " * self.spaces + "{0};".format(bin_op.accept(self.plain)))

    def visitUnaryOperation(self, un_op):
        print(" " * self.spaces + "{0};".format(un_op.accept(self.plain)))

    def visitFunctionCall(self, fun_call):
        print(" " * self.spaces + "{0};".format(fun_call.accept(self.plain)))


def example():
    parent = Scope()
    parent["foo"] = Function(('hello', 'world'),
                             [Print(BinaryOperation(Reference('hello'),
                                                    '+',
                                                    Reference('world')))])
    parent["bar"] = Number(10)
    scope = Scope(parent)
    assert 10 == scope["bar"].value
    scope["bar"] = Number(20)
    assert scope["bar"].value == 20
    printer = PrettyPrinter()
    #print('It should print 2: ', end=' ')
    printer.visit(FunctionDefinition("foo", scope["foo"]))
    printer.visit(FunctionCall(Reference("foo"),
                 [Number(5), UnaryOperation('-', Number(3))]))

def mytest():
    printer = PrettyPrinter()
    scope = Scope()
   # Read('a').evaluate(scope)
   # Read('b').evaluate(scope)
    printer.visit(
    Conditional(BinaryOperation(BinaryOperation(BinaryOperation(
                                  Reference("a"),"+",Reference("b")), "%", Number(2)), "==", Number(0)), 
        [Print(BinaryOperation(Reference("a"),"*",Reference("b")))], #else
        [Print(UnaryOperation("-", Reference("a")))])
    )

if __name__ == "__main__":
    example()
    mytest()
