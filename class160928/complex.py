class ComplexNumber:
    
    def __init__(self, re = 0, im = 0):
        self.re = re
        self.im = im
    
    def __add__(self, num):
        if not isinstance(num, ComplexNumber):
            num = ComplexNumber(num)
        return ComplexNumber(self.re + num.re, self.im + num.im)

    def __sub__(self, num):
        if not isinstance(num, ComplexNumber):
            num = ComplexNumber(num)
        return ComplexNumber(self.re - num.re, self.im - num.im)

    def __mul__(self, num):
        if not isinstance(num, ComplexNumber):
            num = ComplexNumber(num)
        return ComplexNumber(self.re * num.re - self.im * num.im, self.im * num.re + num.im * self.re)

    def __truediv__(self, num):
        if not isinstance(num, ComplexNumber):
            num = ComplexNumber(num)
        temp = self * ComplexNumber(num.re, -num.im)
        div = num.re**2 + num.im**2
        if div == 0:
            raise ZeroDivisionError
        return ComplexNumber(temp.re/div, temp.im/div)

    def __pow__(self, num):
        if isinstance(num, int):
            if num >= 0:
                res = ComplexNumber(1)
                for i in range(num):
                    res *= self
                return res
            if num < 0:
                num = -num
                res = ComplexNumber(1)
                for i in range(num):
                    res *= self
                return ComplexNumber(1)/res
        else:
            raise NotImplementedError

    def __iadd__(self, num):
        self = self + num
        return self

    def __isub__(self, num):
        self = self - num
        return self
    
    def __imul__(self, num):
        self = self * num
        return self

    def __itruediv__(self, num):
        self = self / num
        return self

    def __ipow__(self, num):
        self = self**num
        return self

    def __abs__(self):
        return (self.re**2 + self.im**2)**(0.5)

    def __str__(self):
        return "(" + str(self.re) + " + " + str(self.im) + "i)"

    def __repr__(self):
        return self.__str__();
