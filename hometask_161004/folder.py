from model import *
from printer import *

class ConstantFolder:
    def __init__(self):
        self.visiter = ConstantFolderVisiter()
    def visit(self, tree):
        return tree.accept(self.visiter)

class ConstantFolderVisiter:
    def visitBinaryOperation(self, bin_op):
        bin_op = BinaryOperation(bin_op.lhs.accept(self), bin_op.op, bin_op.rhs.accept(self))
        if(isinstance(bin_op.lhs, Number) and isinstance(bin_op.rhs, Number)):
            return bin_op.evaluate(None)
        if(isinstance(bin_op.lhs, Number) and bin_op.lhs.value == 0 and isinstance(bin_op.rhs, Reference) and bin_op.op == '*'):
            return Number(0)
        if(isinstance(bin_op.rhs, Number) and bin_op.rhs.value == 0 and isinstance(bin_op.lhs, Reference) and bin_op.op == '*'):
            return Number(0)
        if(isinstance(bin_op.lhs, Reference) and isinstance(bin_op.rhs, Reference) and bin_op.lhs.name == bin_op.rhs.name):
            return Number(0)
        return bin_op

    def visitUnaryOperation(self, un_op):
        un_op = UnaryOperation(un_op.op, un_op.expr.accept(self))
        if(isinstance(un_op.expr, Number)):
            return un_op.evaluate(None)
        return un_op

    def visitPrint(self, print_s):
        return Print(print_s.expr.accept(self))

    def visitRead(self, read_s):
        return read_s;

    def visitNumber(self, num):
        return num

    def visitReference(self, ref):
        return ref

    def visitFunctionDefinition(self, fun_def):
        return FunctionDefinition(fun_def.name, fun_def.function.accept(self))
        
    def visitFunction(self, func):
        return Function(func.args, [expr.accept(self) for expr in func.body])

    def visitFunctionCall(self, fun_call):
        return FunctionCall(fun_call.fun_expr.accept(self), [expr.accept(self) for expr in fun_call.args])

    def visitConditional(self, cond):
        return Conditional(cond.condition.accept(self), [expr.accept(self) for expr in cond.if_true], None if cond.if_false == None else [expr.accept(self) for expr in cond.if_false])


def example():
    printer = PrettyPrinter()
    folder = ConstantFolder()
    printer.visit(folder.visit(Print(BinaryOperation(Number(2), '*', UnaryOperation('-', BinaryOperation(Number(0), '*', Reference("x")))))))

if __name__ == '__main__':
    example()
