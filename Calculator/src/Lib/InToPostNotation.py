__author__ = 'yuri'
import re


class InToPostNotation():
    # Create a reverse polish notation ( 3+2 -> 3 2 +)
    def __init__(self):
        self.__output = ''

    def get_rpn(self, expr):
        # Generate RPN
        space = False
        pos = 0
        sl = 0
        stack = []
        expr = self.__check_expr(expr)
        self.__clear_output()
        while pos < len(expr):
            token = expr[pos]
            # If token is number -> add to the output string
            if self.__is_number(token) is True:
                self.__set_output(token, space)
                space = False
            #If token is function -> grab function name and add into the stack
            elif self.__is_function(token):
                func = ''
                while self.__is_function(token):
                    func += token
                    pos += 1
                    token = expr[pos]
                #Mark function with F
                self.__set_output(self.function_flag, space)
                space = True
                stack.insert(sl, func)
                sl += 1
                pos -= 1
            #If the delimiter of arguments
            elif token == ',':
                space = True
                pe = False
                while sl > 0:
                    stack_token = stack[sl - 1]
                    if stack_token == self.left_bracket:
                        pe = True
                        break
                    else:
                        self.__set_output(stack_token)
                        sl -= 1
                if pe is False:
                    raise Exception("Error: separator or parentheses mismatched")
            #If the operator -> add to the stack or add to the output string
            elif self.is_operator(token) is True:
                while sl > 0:
                    stack_token = stack[sl - 1]
                    if self.is_operator(stack_token) is True and self.check_prior(token) < self.check_prior(
                            stack_token):
                        self.__set_output(stack_token)
                        sl -= 1
                    else:
                        break
                stack.insert(sl, token)
                self.__set_output(' ', False)
                sl += 1
            elif token == self.left_bracket:
                stack.insert(sl, token)
                sl += 1
            elif token == self.right_bracket:
                pe = False
                while sl > 0:
                    stack_token = stack[sl - 1]
                    if stack_token == self.left_bracket:
                        pe = True
                        break
                    else:
                        self.__set_output(stack_token)
                        sl -= 1
                if pe is False:
                    raise Exception("Error: parentheses mismatched")
                sl -= 1
                if sl > 0:
                    stack_token = stack[sl - 1]
                    if self.__is_function(stack_token):
                        self.__set_output(stack_token)
                        sl -= 1
            else:
                raise Exception("Unknown token: " + token)
            pos += 1
        # Adds latest values to the output string
        while sl > 0:
            stack_token = stack[sl - 1]
            if stack_token == self.left_bracket or stack_token == self.right_bracket:
                raise Exception("Error: parentheses mismatched")
            self.__set_output(stack_token)
            sl -= 1
        return self.__get_output()

    def __check_expr(self, expr):
        # Removes white spaces
        rg = re.compile(r'\s+')
        expr = rg.sub('', expr)
        mapping = [('(-', '(0-'), (',-', ',0-'), ('(+', '(0+'), (',+', ',0+')]
        for k, v in mapping:
            expr = expr.replace(k, v)
        if expr[0] == '-' or expr[0] == '+':
            expr = '0' + expr
        return expr

    def __set_output(self, symbol, space=True):
        # Generate output string in RPN
        if space is True:
            space = ' '
        else:
            space = ''
        self.__output += space + symbol

    def __is_number(self, symbol):
        # Checks a token
        return True if symbol.isdigit() or symbol == '.' else False

    def __is_function(self, symbol):
        # Is the token a function
        return True if symbol.lower().isalnum() else False

    def __clear_output(self):
        # Resets RPN
        self.__output = ''

    def __get_output(self):
        # Retrieves RPN
        print self.__output
        return self.__output