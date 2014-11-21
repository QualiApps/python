__author__ = 'yuri'
import math


class Actions():
    def __init__(self):
        self.function_flag = 'F'
        self.left_bracket = '('
        self.right_bracket = ')'
        self.prior = {'*': 4, '/': 4, '%': 4, '-': 3, '+': 2, '=': 1}
        self.operators = {
            '+': self.plus,
            '-': self.minus,
            '*': self.multiply,
            '/': self.divide,
            '%': self.divide_by_module
        }

    def action(self, operand_a, operand_b, token):
        # Execute for operators
        return self.operators[token](operand_a, operand_b)

    def function(self, args, name):
        # Execute for functions
        if self.check_function(name, math):
            function = getattr(math, name)
        elif self.check_function(name, self):
            function = getattr(self, name)
        else:
            raise Exception("Unsupported function of the expression: " + name)
        return function(*args)

    def is_function(self, function):
        # Check if function
        return True if self.check_function(function, math) or self.check_function(function, self) else False

    def check_function(self, name, obj):
        # If function is available
        return True if name in dir(obj) else False

    def is_operator(self, symbol):
        # Check if operator
        result = False
        if symbol in self.operators:
            result = True
        return result

    def check_prior(self, symbol):
        # Check priority
        return self.prior.get(symbol, (lambda: 0)())

    def plus(self, op_a, op_b):
        # Plus action
        return op_a + op_b

    def minus(self, op_a, op_b):
        # Minus action
        return op_a - op_b

    def multiply(self, op_a, op_b):
        # Multiply action
        return op_a * op_b

    def divide(self, op_a, op_b):
        # Divide action
        return op_a / op_b

    def divide_by_module(self, op_a, op_b):
        # Divide action by module
        return op_a % op_b

    def f(self, a, b):
        # Custom function
        return a + b