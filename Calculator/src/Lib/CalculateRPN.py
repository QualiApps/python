__author__ = 'yuri'
from Operators import Operators


class CalculateRPN(Operators):
	def __init__(self):
		Operators.__init__(self)

	#Calculate RPN
	def calculate_rpn(self, rpn):
		stack = []
		rpn = rpn.split()
		position = 0
		while position < len(rpn):
			token = rpn[position]
			#If operator
			if token in self.operators:
				if len(stack) < 2:
					raise Exception("Insufficient data on the stack for the operation: " + token)
				op_b = stack.pop()
				op_a = stack.pop()
				result = self.execute(op_a, op_b, token)
				stack.append(result)
			#If function
			elif token in self.functions:
				args = []
				while True:
					operand = stack.pop()
					if operand == self.function_flag:
						args.reverse()
						break
					args.append(operand)
				result = self.execute_function(args, token)
				stack.append(result)
			#If number
			elif self.is_digit(token) is True:
				stack.append(float(token))
			#If start flag of function
			elif token == self.function_flag:
				stack.append(token)
				position += 1
				continue
			else:
				raise Exception("Invalid character in the expression: " + token)
			position += 1
		if len(stack) > 1:
			raise Exception("The number of operators does not match to the number of operands: " + token)
		return stack.pop()

	#Check if number
	def is_digit(self, number):
		try:
			float(number)
			digit = True
		except:
			digit = False
		finally:
			return digit