__author__ = 'yuri'
import re
from Lib import Calculator


#Removes white spaces
def clear_string(string):
	rg = re.compile(r'\s+')
	return rg.sub('', string)


calc = Calculator.Calculator()
print "Expression for calculation ( ex: (5+5)*5/sin(.5)+sqrt(25) ):"
while True:
	# Remove all white spaces
	cleanString = clear_string(raw_input("Enter your expression: "))
	#Exit action
	if cleanString == 'exit':
		break
	try:
		result = calc.calculate(cleanString)
	except Exception as e:
		result = e
	finally:
		print "Result =", result