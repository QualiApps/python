__author__ = 'yuri'
from Lib.InToPostNotation import InToPostNotation
from Lib.CalculateRPN import CalculateRPN
import sys


def calculate(string):
    try:
        rpn = InToPostNotation().get_rpn(string)
        result = string + " = " + str(CalculateRPN().calculate_expr(rpn))
    except IndexError:
        result = 'Syntax Error: invalid syntax'
    except Exception as e:
        result = e
    finally:
        print result

if len(sys.argv) > 1:
    """If the file of expressions"""
    try:
        fe = open(sys.argv[1])
        for expr in fe.read().splitlines():
            calculate(expr)
    except IOError as io:
        print io
else:
    print "Expression for calculation ( ex: (5+5)*5/sin(.5)+sqrt(25) ):"
    while True:
        try:
            expression = raw_input("Enter your expression: ")
            # Exit action
            if expression in ('exit', 'quit'):
                break
            else:
                calculate(expression)
        except KeyboardInterrupt:
            exit()