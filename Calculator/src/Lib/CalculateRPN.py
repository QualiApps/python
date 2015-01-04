__author__ = 'yuri'
import __builtin__ as builtin
import math
import operator


class CalculateRPN(object):
    """This instance to calculate RPN expression"""
    __instance = None

    def __init__(self, flag='F', unary='_'):
        if not self.__initialized:
            self.__number = 0
            self.unary_symbol = unary
            self.operators = {self.unary_symbol: 'neg', '**': 'pow', '^': 'pow', '*': 'mul', '/': 'div',
                              '//': 'floordiv', '%': 'mod', '-': 'sub', '+': 'add'}
            self.function_flag = flag
            self.__initialized = True

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(CalculateRPN, cls).__new__(cls, *args, **kwargs)
            cls.__instance.__initialized = False
        return cls.__instance

    def calculate_expr(self, rpn):
        """Calculate RPN"""
        stack = []
        rpn = rpn.split()
        position = 0
        while position < len(rpn):
            token = rpn[position]
            # If operator
            if token in self.operators:
                if token == self.unary_symbol:
                    stack.append(self.action(token, stack.pop()))
                else:
                    if len(stack) < 2:
                        raise Exception("Invalid syntax near the operator: " + token)
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(self.action(token, a, b))
            # If function
            elif self.is_function(token):
                args = list()
                while True:
                    argument = stack.pop()
                    if argument == self.function_flag:
                        args.reverse()
                        break
                    args.append(argument)
                stack.append(self.function(token, args))
            # If number
            elif self.digit(token):
                stack.append(self.__number)
            # If start flag of function
            elif token == self.function_flag:
                stack.append(token)
            else:
                raise Exception("Invalid character in the expression: " + token)
            position += 1
        if len(stack) > 1:
            raise Exception("The number of operators does not match to the number of operands: " + token)
        return stack.pop()

    def digit(self, number):
        """Check if number"""
        try:
            self.__number = int(number) if number.isdigit() else float(number)
            digit = True
        except ValueError:
            digit = False
        finally:
            return digit

    def action(self, token, *args):
        """Execute for operators"""
        action = getattr(operator, self.operators.get(token))
        return action(*args)

    def function(self, name, args):
        """Execute for functions"""
        if self.check_function(name, math):
            function = getattr(math, name)
        elif self.check_function(name, self):
            function = getattr(self, name)
        elif self.check_function(name, builtin):
            function = getattr(builtin, name)
        else:
            raise Exception("Unsupported function of the expression: " + name)
        return function(*args)

    def is_function(self, function):
        """Check if function"""
        return True if self.check_function(function, math) or self.check_function(function, self) \
                       or self.check_function(function, builtin) else False

    @staticmethod
    def check_function(name, obj):
        """If function is available"""
        return True if name in dir(obj) else False

    @staticmethod
    def f(a, b):
        """Custom function"""
        return a + b