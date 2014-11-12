__author__ = 'yury'
import re
from Component import Calculator

calc = Calculator.Calculator()
while (True):
    # Remove all white spaces
    cleanString = re.sub(r'\s', '', input("Enter an expression for calculation (ex: 5+23): "))
    if cleanString == 'exit':
        break
    result = calc.calculate(cleanString)
    print(result)
