__author__ = 'yuri'
from Lib.InToPostNotation import InToPostNotation
from Lib.CalculateRPN import CalculateRPN

print "Expression for calculation ( ex: (5+5)*5/sin(.5)+sqrt(25) ):"
while True:
    expression = raw_input("Enter your expression: ")
    # Exit action
    if expression == 'exit':
        break
    try:
        rpn = InToPostNotation().get_rpn(expression)
        result = "Result = " + str(CalculateRPN().calculate_expr(rpn))
    except Exception as e:
        result = e
    finally:
        print result