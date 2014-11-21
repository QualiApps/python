__author__ = 'yuri'
from Actions import Actions


class CalculateRPN(Actions):
    def __init__(self):
        Actions.__init__(self)
        self.__number = 0

    def calculate_rpn(self, rpn):
        # Calculate RPN
        stack = []
        rpn = rpn.split()
        position = 0
        while position < len(rpn):
            token = rpn[position]
            #If operator
            if token in self.operators:
                if len(stack) < 2:
                    raise Exception("Invalid syntax near operator: " + token)
                op_b = stack.pop()
                op_a = stack.pop()
                stack.append(self.action(op_a, op_b, token))
            #If function
            elif self.is_function(token):
                args = []
                while True:
                    argument = stack.pop()
                    if argument == self.function_flag:
                        args.reverse()
                        break
                    args.append(argument)
                stack.append(self.function(args, token))
            #If number
            elif self.__digit(token):
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

    def __digit(self, number):
        # Check if number
        try:
            self.__number = float(number)
            digit = True
        except ValueError:
            digit = False
        finally:
            return digit