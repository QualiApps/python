__author__ = 'yuri'
import re
from Calculator import Calculator

calc = Calculator()
print "Expression for calculation ( ex: (5+5)*5/sin(.5)+sqrt(25) ):"
while True:
    expression = raw_input("Enter your expression: ")
    # Exit action
    if expression == 'exit':
        break
    #try:
    result = "Result = " + str(calc.calculate(expression))
    #except Exception as e:
    #    result = e
    #finally:
    print result