__author__ = 'yuri'
import re
import math


class InToPostNotation():
    """Create a reverse polish notation ( 3+2 -> 3 2 +, or 3+2+function(1,2) -> 3 2 F 1 2 function + +)"""
    _instance = None

    def __init__(self, flag='F', unary='_'):
        self.__expression = ''
        self.__output = ''
        self.function_flag = flag  # The start flag of the function arguments
        self.args_separator = ','  # The delimiter of the function arguments
        self.unary_symbol = unary
        self.left_bracket = '('
        self.right_bracket = ')'
        # Available operators and their precedences
        self.operators = {self.unary_symbol: 6, '^': 6, '**': 6, '*': 4, '/': 4, '//': 4, '%': 4, '-': 2, '+': 2}
        self.pm_operators = ('-', '+')
        self.hp_operators = ('^', '*', '/', '%')

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(InToPostNotation, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def get_rpn(self, expr):
        """Generate RPN"""
        space = False
        current = 0
        stack_size = 0
        stack = []
        self.__expression = self.remove_spaces(expr)
        self.__clear_output()
        while current < len(self.__expression):
            self.__check_expr(current)
            token = self.__expression[current]
            # If token is number -> add to the output string
            if self.__is_number(token) is True:
                self.__set_output(token, space)
                self.__check_expr_mul(current)
                space = False
            # If token is function -> grab function name and add into the stack
            elif self.__is_function(token):
                math_const = self.__is_math_const(current)
                if math_const[0]:
                    self.__set_output(math_const[0], space)
                    current = math_const[1]
                    self.__check_expr_mul(current)
                else:
                    func = ''
                    while self.__is_function(token):
                        func += token
                        current += 1
                        token = self.__expression[current]
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
                # Check if a double operator
                if current < len(self.__expression) - 1 and self.__expression[current + 1] == token and \
                        self.__is_operator(token + self.__expression[current + 1]) is True:
                    token = token + self.__expression[current + 1]
                    self.__expression = self.__expression[:current] + self.__expression[current + 1:]
                while stack_size > 0:
                    stack_token = stack[stack_size - 1]
                    if self.__is_operator(stack_token) is True \
                            and (((self.__left_assoc(token) is True and (
                                self.__check_prior(token) <= self.__check_prior(stack_token)))
                            or (self.__left_assoc(token) is False and (
                                self.__check_prior(token) < self.__check_prior(stack_token))))):
                        self.__set_output(stack_token)
                        stack_size -= 1
                    else:
                        break
                stack.insert(stack_size, token)
                stack_size += 1
                self.__set_output(' ', False)
            elif token == self.left_bracket:
                stack.insert(stack_size, token)
                stack_size += 1
            elif token == self.right_bracket:
                self.__check_expr_mul(current)
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
        """Generate output string in RPN"""
        space = ' ' if space is True else ''
        self.__output += space + symbol

    def __clear_output(self):
        """Resets RPN"""
        self.__output = ''

    def __get_output(self):
        """Retrieves RPN"""
        #print self.__output
        return self.__output

    def __check_prior(self, symbol):
        """Check priority"""
        return self.operators.get(symbol, (lambda: 0)())

    def __left_assoc(self, symbol):
        """Check assoc (if unary simbol that is right-assoc)"""
        return False if symbol in (self.unary_symbol, '**', '^') else True

    def __is_operator(self, symbol):
        """Check if operator"""
        return True if symbol in self.operators else False

    def __is_math_const(self, pos):
        """Checks the math constants"""
        constant = ''
        current = pos
        while current < len(self.__expression) and self.__expression[current].isalpha():
            constant += self.__expression[current]
            current += 1
        if hasattr(math, constant) and not callable(getattr(math, constant)):
            constant = str(getattr(math, constant))
            pos = current - 1
        else:
            constant = ''
        return constant, pos

    def __check_expr(self, pos):
        """Checks the sign of the operand and changes multi operators"""
        current = pos
        sign = ''
        if self.__expression[pos] in self.pm_operators:
            while self.__expression[current] in self.pm_operators:
                if (self.__expression[current] == self.pm_operators[1] and sign == self.pm_operators[0]) \
                        or (self.__expression[current] == self.pm_operators[0] and sign != self.pm_operators[0]):
                    sign = self.pm_operators[0]
                else:
                    sign = self.pm_operators[1]
                current += 1
        u_minus = sign
        if pos == 0 or pos > 0 and self.__expression[pos - 1] in (self.left_bracket, self.args_separator) \
                or self.__expression[pos - 1] in self.hp_operators:
            u_minus = self.unary_symbol if sign == self.pm_operators[0] else ''
        self.__expression = self.__expression[:pos] + u_minus + self.__expression[current:]

    def __check_expr_mul(self, pos):
        """Adds the '*' to the input expression if it includes 3(...; 3function(; or )6"""
        if pos < len(self.__expression) - 1:
            if self.__expression[pos + 1].lower().isalpha() or self.__expression[pos + 1] == self.left_bracket \
                    or (self.__expression[pos] == self.right_bracket
                        and self.__is_number(self.__expression[pos + 1]) is True):
                self.__expression = self.__expression[:pos + 1] + self.hp_operators[1] + self.__expression[pos + 1:]

    @staticmethod
    def remove_spaces(expr):
        """Removes white spaces"""
        rg = re.compile(r'\s+')
        return rg.sub('', expr)

    @staticmethod
    def __is_number(symbol):
        """Checks a token"""
        return True if symbol.isdigit() or symbol == '.' else False

    @staticmethod
    def __is_function(symbol):
        """Is the token a function"""
        return True if symbol.lower().isalnum() else False