__author__ = 'yuri'
import math
import operator


class CalculateRPN():
    def __init__(self, operators, flag='F'):
        self.__number = 0
        self.operators = operators
        self.function_flag = flag

    def calculate_expr(self, rpn):
        # Calculate RPN
        stack = []
        rpn = rpn.split()
        position = 0
        while position < len(rpn):
            token = rpn[position]
            # If operator
            if token in self.operators:
                if len(stack) < 2:
                    raise Exception("Invalid syntax near operator: " + token)
                args = list()
                args.append(stack.pop())
                args.append(stack.pop())
                args.reverse()
                stack.append(self.action(args, token))
            # If function
            elif self.is_function(token):
                args = list()
                while True:
                    argument = stack.pop()
                    if argument == self.function_flag:
                        args.reverse()
                        break
                    args.append(argument)
                stack.append(self.function(args, token))
            #If number
            elif self.digit(token):
                stack.append(self.__number)
            #If start flag of function
            elif token == self.function_flag:
                stack.append(token)
            else:
                raise Exception("Invalid character in the expression: " + token)
            position += 1
        if len(stack) > 1:
            raise Exception("The number of operators does not match to the number of operands: " + token)
        return stack.pop()

    def digit(self, number):
        # Check if number
        try:
            self.__number = float(number)
            digit = True
        except ValueError:
            digit = False
        finally:
            return digit

    def action(self, args, token):
        # Execute for operators
        prior, action = self.operators.get(token)
        action = getattr(operator, action)
        return action(*args)

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

    @staticmethod
    def check_function(name, obj):
        # If function is available
        return True if name in dir(obj) else False

    @staticmethod
    def f(a, b):
        # Custom function
        return a + b