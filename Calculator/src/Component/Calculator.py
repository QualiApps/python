__author__ = 'yury'


class Calculator():
    __result = __position = 0
    __error = False

    def __init__(self):
        self.operators = {'+': self.plus, '-': self.minus, '*': self.multiply, '/':self.divide}

    #Calculate the expression
    def calculate(self, expr):
        self.rewindExprPosition()
        self.__result = self.__getNumber(expr)
        while (self.getExprPosition() < len(expr)):
            if (self.__isOperator(expr[self.getExprPosition()]) == True):
                self.operators[expr[self.getExprPosition()]](expr)
            else:
                self.incrementExprPosition()
        return self.__gerResult()

    #Retrieves a number or check it
    def __getNumber(self, expr, position = 0):
        number = ''
        while (position < len(expr)):
            if (self.__isOperator(expr[position]) == True):
                break
            number += expr[position]
            position += 1
            self.setExprPosition(position)
        try:
            number = int(number)
        except:
            number = 0
            self.__error = True
            print('Expression error: the symbol must be a numeric or wrong operator!')
        finally:
            return number

    #Checks operators
    def __isOperator(self, symbol):
        try:
            result = False
            symbol = int(symbol)
        except:
            if (symbol in self.getOperators()):
                result = True
        finally:
            return result

    #Plus action
    def plus(self, expr):
        self.incrementExprPosition()
        self.__result = self.__result + self.__getNumber(expr, self.getExprPosition())

    #Minus action
    def minus(self, expr):
        self.incrementExprPosition()
        self.__result = self.__result - self.__getNumber(expr, self.getExprPosition())

    #Multiply action
    def multiply(self, expr):
        self.incrementExprPosition()
        self.__result = self.__result * self.__getNumber(expr, self.getExprPosition())

    #Divide action
    def divide(self, expr):
        self.incrementExprPosition()
        self.__result = self.__result / self.__getNumber(expr, self.getExprPosition())

    #Retrieves position of expr
    def getExprPosition(self):
        return self.__position

    #Sets position of expr
    def setExprPosition(self, index = 0):
        self.__position = index

    #Resets position of expr to 0
    def rewindExprPosition(self):
        self.setExprPosition()

    #Increments position of expr
    def incrementExprPosition(self):
        self.setExprPosition(self.getExprPosition() + 1)

    #Retrieves available operators
    def getOperators(self):
        return self.operators

    #Gets result
    def __gerResult(self):
        response = 'Result: %s' % (self.__result)
        if (self.__error == True):
            self.__error = False
            response = ''
        return response