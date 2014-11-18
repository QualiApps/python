__author__ = 'yuri'
from InToPostNotation import InToPostNotation


class Calculator(InToPostNotation):
	def __init__(self):
		InToPostNotation.__init__(self)

	def calculate(self, expr):
		return self.exec_action(expr)
