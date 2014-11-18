__author__ = 'yuri'
import math


class Operators():
    def __init__(self):
        self.function_flag = 'F'
        self.left_bracket = '('
        self.right_bracket = ')'
        self.prior = {'*': 3, '/': 3, '%': 3, '+': 2, '-': 2, '=': 1}
        self.operators = {
            '+': self.plus,
            '-': self.minus,
            '*': self.multiply,
            '/': self.divide,
            '%': self.divide_by_module
        }
        self.functions = {
            # Core functions  #You may implement more functions here
            'log': math.log,
            'sqrt': math.sqrt,
            'sin': math.sin,
            'cos': math.cos,  # Custom functions
            'f': self.f
        }

    def execute(self, operand_a, operand_b, token):
        # Execute for operators
        return self.operators[token](operand_a, operand_b)

    def execute_function(self, args, token):
        # Execute for functions
        return self.functions[token](*args)

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