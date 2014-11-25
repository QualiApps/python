__author__ = 'yuri'
import re


class InToPostNotation():
    # Create a reverse polish notation ( 3+2 -> 3 2 +, or 3+2+function(1,2) -> 3 2 F 1 2 function + +)
    def __init__(self, operators, flag='F'):
        self.__output = ''
        self.function_flag = flag  # The start flag of the function arguments
        self.args_separator = ','  # The delimiter of the function arguments
        self.left_bracket = '('
        self.right_bracket = ')'
        self.operators = operators  # Available operators and their precedences, actions

    def get_rpn(self, expr):
        # Generate RPN
        space = False
        current = 0
        stack_size = 0
        stack = []
        expr = self.__check_expr(expr)
        self.__clear_output()
        while current < len(expr):
            token = expr[current]
            # If token is number -> add to the output string
            if self.__is_number(token) is True:
                self.__set_output(token, space)
                space = False
            # If token is function -> grab function name and add into the stack
            elif self.__is_function(token):
                func = ''
                while self.__is_function(token):
                    func += token
                    current += 1
                    token = expr[current]
                # Mark function with F
                self.__set_output(self.function_flag, space)
                space = True
                stack.insert(stack_size, func)
                stack_size += 1
                current -= 1
            # If the delimiter of arguments
            elif token == self.args_separator:
                space = True
                check = False
                while stack_size > 0:
                    stack_token = stack[stack_size - 1]
                    if stack_token == self.left_bracket:
                        check = True
                        break
                    else:
                        self.__set_output(stack_token)
                        stack_size -= 1
                if check is False:
                    raise Exception("Error: separator or parentheses mismatched")
            # If the operator -> add to the stack or add to the output string
            elif self.__is_operator(token) is True:
                while stack_size > 0:
                    stack_token = stack[stack_size - 1]
                    if self.__is_operator(stack_token) is True \
                            and self.__check_prior(token) < self.__check_prior(stack_token):
                        self.__set_output(stack_token)
                        stack_size -= 1
                    else:
                        break
                # Check if a double operator
                if len(stack) > stack_size and stack[stack_size] == token:
                    stack[stack_size] += token
                else:
                    stack.insert(stack_size, token)
                if current + 1 <= len(expr) and expr[current + 1] == token \
                        and self.__is_operator(token + expr[current + 1]) is True:
                    delimiter = ''
                else:
                    delimiter = ' '
                    stack_size += 1
                self.__set_output(delimiter, False)
            elif token == self.left_bracket:
                stack.insert(stack_size, token)
                stack_size += 1
            elif token == self.right_bracket:
                check = False
                while stack_size > 0:
                    stack_token = stack[stack_size - 1]
                    if stack_token == self.left_bracket:
                        check = True
                        break
                    else:
                        self.__set_output(stack_token)
                        stack_size -= 1
                if check is False:
                    raise Exception("Error: parentheses mismatched")
                stack_size -= 1
                if stack_size > 0:
                    stack_token = stack[stack_size - 1]
                    if self.__is_function(stack_token):
                        self.__set_output(stack_token)
                        stack_size -= 1
            else:
                raise Exception("Unknown token: " + token)
            current += 1
        # Adds latest values to the output string
        while stack_size > 0:
            stack_token = stack[stack_size - 1]
            if stack_token == self.left_bracket or stack_token == self.right_bracket:
                raise Exception("Error: parentheses mismatched")
            self.__set_output(stack_token)
            stack_size -= 1
        return self.__get_output()

    def __set_output(self, symbol='', space=True):
        # Generate output string in RPN
        space = ' ' if space is True else ''
        self.__output += space + symbol

    def __clear_output(self):
        # Resets RPN
        self.__output = ''

    def __get_output(self):
        # Retrieves RPN
        return self.__output

    def __check_prior(self, symbol):
        # Check priority
        prior, action = self.operators.get(symbol, (lambda: 0)())
        return prior

    def __is_operator(self, symbol):
        # Check if operator
        return True if symbol in self.operators else False

    @staticmethod
    def __check_expr(expr):
        # Removes white spaces
        rg = re.compile(r'\s+')
        expr = rg.sub('', expr)
        mapping = [('(-', '(0-'), (',-', ',0-'), ('(+', '(0+'), (',+', ',0+')]
        for k, v in mapping:
            expr = expr.replace(k, v)
        expr = '0' + expr if expr[0] == '-' or expr[0] == '+' else expr
        return expr

    @staticmethod
    def __is_number(symbol):
        # Checks a token
        return True if symbol.isdigit() or symbol == '.' else False

    @staticmethod
    def __is_function(symbol):
        # Is the token a function
        return True if symbol.lower().isalnum() else False