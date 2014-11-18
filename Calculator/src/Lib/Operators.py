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
			#Core functions
			#You may implement more functions here
			'log': math.log,
			'sqrt': math.sqrt,
			'sin': math.sin,
			'cos': math.cos,
			#Custom functions
			'f': self.f
		}

	#Execute for operators
	def execute(self, operand_a, operand_b, token):
		return self.operators[token](operand_a, operand_b)

	#Execute for functions
	def execute_function(self, args, token):
		return self.functions[token](*args)

	#Check if operator
	def is_operator(self, symbol):
		result = False
		if symbol in self.operators:
			result = True
		return result

	#Check priority
	def check_prior(self, symbol):
		return self.prior.get(symbol, (lambda: 0)())

	# Plus action
	def plus(self, op_a, op_b):
		return op_a + op_b

	# Minus action
	def minus(self, op_a, op_b):
		return op_a - op_b

	# Multiply action
	def multiply(self, op_a, op_b):
		return op_a * op_b

	# Divide action
	def divide(self, op_a, op_b):
		return op_a / op_b

	# Divide action by module
	def divide_by_module(self, op_a, op_b):
		return op_a % op_b

	# Custom function
	def f(self, a, b):
		return a+b