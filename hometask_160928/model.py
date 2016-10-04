#!/usr/bin/env python3
# Шаблон для домашнѣго задания
# Рѣализуйте мѣтоды с raise NotImplementedError

class Scope:

    """Scope - представляет доступ к значениям по именам
    (к функциям и именованным константам).
    Scope может иметь родителя, и если поиск по имени
    в текущем Scope не успешен, то если у Scope есть родитель,
    то поиск делегируется родителю.
    Scope должен поддерживать dict-like интерфейс доступа
    (см. на специальные функции __getitem__ и __setitem__)
    """

    def __init__(self, parent=None):
        self.parent = parent
        self.curObjects = dict()
    
    def __getitem__(self, item):
        if not item in self.curObjects and self.parent:
            return self.parent[item]
        return self.curObjects[item]

    def __setitem__(self, item, val):
        self.curObjects[item] = val

class Number:

    """Number - представляет число в программе.
    Все числа в нашем языке целые."""

    def __init__(self, value):
        if not isinstance(value, int):
            value = int(value)
        self.value = value

    def evaluate(self, scope):
        return self


class Function:

    """Function - представляет функцию в программе.
    Функция - второй тип поддерживаемый языком.
    Функции можно передавать в другие функции,
    и возвращать из функций.
    Функция состоит из тела и списка имен аргументов.
    Тело функции это список выражений,
    т. е.  у каждого из них есть метод evaluate.
    Во время вычисления функции (метод evaluate),
    все объекты тела функции вычисляются последовательно,
    и результат вычисления последнего из них
    является результатом вычисления функции.
    Список имен аргументов - список имен
    формальных параметров функции."""

    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        for expression in self.body[:-1]:
            expression.evaluate(scope)
        return self.body[-1].evaluate(scope)


class FunctionDefinition:

    """FunctionDefinition - представляет определение функции,
    т. е. связывает некоторое имя с объектом Function.
    Результатом вычисления FunctionDefinition является
    обновление текущего Scope - в него
    добавляется новое значение типа Function."""

    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function


class Conditional:

    """
    Conditional - представляет ветвление в программе, т. е. if.
    """

    def __init__(self, condition, if_true, if_false=None):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        if self.condition.evaluate(scope).value == 0:
            #if_false
            if self.if_false == None:
                return None
            for expression in self.if_false[:-1]:
                expression.evaluate(scope)
            return self.if_false[-1].evaluate(scope)
        else:
            #if_true
            if self.if_true == None:
                return None
            for expression in self.if_true[:-1]:
                expression.evaluate(scope)
            return self.if_true[-1].evaluate(scope)



class Print:

    """Print - печатает значение выражения на отдельной строке."""

    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        res = self.expr.evaluate(scope)
        print(res.value)
        return res
        


class Read:

    """Read - читает число из стандартного потока ввода
     и обновляет текущий Scope.
     Каждое входное число располагается на отдельной строке
     (никаких пустых строк и лишних символов не будет).
     """

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        num = Number(int(input()))
        scope[self.name] = num
        return num


class FunctionCall:

    """
    FunctionCall - представляет вызов функции в программе.
    В результате вызова функции должен создаваться новый объект Scope,
    являющий дочерним для текущего Scope
    (т. е. текущий Scope должен стать для него родителем).
    Новый Scope станет текущим Scope-ом при вычислении тела функции.
    """

    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        function = self.fun_expr.evaluate(scope)
        eval_args = []
        for elem in self.args:
            eval_args.append(elem.evaluate(scope))
        call_scope = Scope(scope)
        for i in range(len(self.args)):
            call_scope[function.args[i]] = eval_args[i]
        return function.evaluate(call_scope)


class Reference:

    """Reference - получение объекта
    (функции или переменной) по его имени."""

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]


class BinaryOperation:

    """BinaryOperation - представляет бинарную операцию над двумя выражениями.
    Результатом вычисления бинарной операции является объект Number.
    Поддерживаемые операции:
    “+”, “-”, “*”, “/”, “%”, “==”, “!=”,
    “<”, “>”, “<=”, “>=”, “&&”, “||”."""

    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def evaluate(self, scope):
        lval = self.lhs.evaluate(scope)
        rval = self.rhs.evaluate(scope)
        if self.op == "+":
            return Number(lval.value + rval.value)
        elif self.op == "-":
            return Number(lval.value - rval.value)
        elif self.op == "*":
            return Number(lval.value * rval.value)
        elif self.op == "/":
            return Number(lval.value // rval.value)
        elif self.op == "%":
            return Number(lval.value % rval.value)
        elif self.op == "==":
            return Number(1) if lval.value == rval.value else Number(0)
        elif self.op == "!=":
            return Number(0) if lval.value == rval.value else Number(1)
        elif self.op == "<":
            return Number(1) if lval.value < rval.value else Number(0)
        elif self.op == ">":
            return Number(1) if lval.value > rval.value else Number(0)
        elif self.op == ">=":
            return Number(1) if lval.value >= rval.value else Number(0)
        elif self.op == "<=":
            return Number(1) if lval.value <= rval.value else Number(0)
        elif self.op == "&&":
            return Number(1) if (lval.value != 0) and (rval.value != 0) else Number(0)
        elif self.op == "||":
            return Number(1) if (lval.value != 0) or (rval.value != 0) else Number(0)
        
        

class UnaryOperation:

    """UnaryOperation - представляет унарную операцию над выражением.
    Результатом вычисления унарной операции является объект Number.
    Поддерживаемые операции: “-”, “!”."""

    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        val = self.expr.evaluate(scope)
        if self.op == "-":
            return Number(-val.value)
        if self.op == "!":
            return Number(1) if val.value == 0 else Number(0)


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
    print('It should print 2: ', end=' ')
    FunctionCall(FunctionDefinition('foo', parent['foo']),
                 [Number(5), UnaryOperation('-', Number(3))]).evaluate(scope)

def my_tests():
    scope = Scope()
    Read('a').evaluate(scope)
    Read('b').evaluate(scope)
    Conditional(BinaryOperation(BinaryOperation(BinaryOperation(Reference("a"),"+",Reference("b")), "%", Number(2)), "==", Number(0)), [Print(BinaryOperation(Reference("a"),"*",Reference("b")))],[Print(UnaryOperation("-", Reference("a")))]).evaluate(scope)

if __name__ == '__main__':
    example()
    my_tests()
