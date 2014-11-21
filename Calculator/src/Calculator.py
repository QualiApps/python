__author__ = 'yuri'
from Lib.InToPostNotation import InToPostNotation
from Lib.CalculateRPN import CalculateRPN


class Calculator(InToPostNotation, CalculateRPN):
    def __init__(self):
        InToPostNotation.__init__(self)
        CalculateRPN.__init__(self)

    def calculate(self, expr):
        rpn = self.get_rpn(expr)
        return self.calculate_rpn(rpn)