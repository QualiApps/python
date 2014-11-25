__author__ = 'yuri'
from Lib.InToPostNotation import InToPostNotation
from Lib.CalculateRPN import CalculateRPN


class Calculator(InToPostNotation, CalculateRPN):
    # Available operators and their precedences
    operators = {'**': (4, 'pow'), '*': (3, 'mul'), '/': (3, 'div'),
                 '//': (3, 'floordiv'), '%': (3, 'mod'), '-': (2, 'sub'), '+': (1, 'add')}

    def __init__(self):
        InToPostNotation.__init__(self, self.operators)
        CalculateRPN.__init__(self, self.operators)

    def calculate(self, expr):
        rpn = self.get_rpn(expr)
        return self.calculate_expr(rpn)