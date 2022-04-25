"""
Copyright (C) 2022 Anubosiris
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import math

module_description = """
Class Description:
This class implements simple fractions, based on python's int data type. 
At all times, both the nominator and denominator should be of type int to the outside world.
Floating point numbers and other fractions are not supported internally. However, it is possible to generate a fraction 
by providing a float type nominator to the constructor. The denominator has to be an int type number.
The following methods are implemented:

(OUTGOING METHODS)
Fraction(nominator, denominator) -> constructor, creates Fraction based on given number(s)
- nominator: optional int or float, default is 0
- denominator: optional int, default is 1, cannot be equal 0
getn() -> returns current nominator
getd() -> return current denominator
setn(nominator) -> sets nominator to new int type number
setd(denominator) -> sets denominator to new int type number
print() -> prints a visual representation of the fraction

(TYPE CONVERSION METHODS)
__int__() -> returns int based on the numerical value of the fraction
__str__() -> returns string representation of fraction, also used for print() object method
__float__() -> returns a float type numerical approximation of the fraction (ATTENTION: PRECISION LOSS!)

(ARITHMETIC OPERATORS)
__add__(other) -> implements addition, other can be int, float, or Fraction
__sub__(other) -> implements subtraction, other can be int, float, or Fraction
__mul__(other) -> implements multiplication, other can be int, float, or Fraction
__truediv__(other) -> implements division, other can be int, float, or Fraction
(WRAPPER)
add(other) -> wrapper for __add__(other) object method
sub(other) -> wrapper for __sub__(other) object method
mul(other) -> wrapper for __mul__(other) object method
div(other) -> wrapper for __truediv__(other) object method

(COMPARISON OPERATORS)
__lt__(other) -> checks if numerically less, other can be int, float, or Fraction
__le__(other) -> checks if numerically less or equal, other can be int, float, or Fraction
__eq__(other) -> checks for equality, other can be int, float, or Fraction
__ne__(other) -> checks for inequality, other can be int, float, or Fraction
__ge__(other) -> checks if numerically greater, other can be int, float, or Fraction
__gt__(other) -> checks if numerically greater or equal, other can be int, float, or Fraction
(WRAPPER)
equals(other) -> wrapper for __eq__(other) object method
notequals(other) -> wrapper for __ne__(other) object method
greater(other) -> wrapper for __gt__(other) object method
greaterorequal(other) -> wrapper for __ge__(other) object method
less(other) -> wrapper for __lt__(other) object method
lessorequal(other) -> wrapper for __le__(other) object method

(UNARY OPERATORS)
__pos__() # returns Fraction
__neg__() # returns negative Fraction
__abs__() # returns absolute version of Fraction
__round__(n) # TODO: COMING SOON

(INTERNAL METHODS)
gcd(firstint, secondint) -> static method for used implementation to get the greatest common divisor of 2 ints
deflate() -> shortens the fraction so that equality can be determined correctly
internalMul(integer) -> multiplies both the nominator and the denominator with a given int type number
visualInflation() -> inflates fraction to next int type without loss of floating point precision
"""


class Fraction:
    n = 0  # nominator
    d = 1  # denominator

    # OUTGOING
    def __init__(self, nominator=0, denominator=1):
        assert type(nominator) == int or type(nominator) == float
        assert type(denominator) == int
        assert denominator != 0
        self.n = nominator
        self.d = denominator
        if nominator != 0:
            if type(nominator) == float:
                self.visualInflation()
            else:
                while self.n != int(self.n):
                    self.internalMul(10)
        self.n = int(self.n)
        self.d = int(self.d)
        self.deflate()
        return

    def getn(self):
        return self.n

    def getd(self):
        return self.d

    def setn(self, nominator):
        assert type(nominator) == int  # TODO float support
        self.n = nominator

    def setd(self, denominator):
        assert type(denominator) == int
        assert denominator != 0
        self.d = denominator
        self.deflate()

    def print(self):
        print(self)

    # TYPE CONVERSION
    def __int__(self):
        return int(self.n / self.d)

    def __str__(self):
        self.deflate()
        return f"({self.n}/{self.d})"

    def __float__(self):
        return float(self.n / self.d)

    # ARITHMETIC
    def __add__(self, other):
        if type(other) != Fraction:
            other = Fraction(other)
        assert type(other) == Fraction
        result = Fraction(1)
        a = self
        b = other
        m = self.d * other.d
        result.n = (a.n * b.d) + (b.n * a.d)
        result.d = m
        result.deflate()
        return result

    def __sub__(self, other):
        if type(other) != Fraction:
            other = Fraction(other)
        assert type(other) == Fraction
        result = Fraction(1)
        a = self
        b = other
        m = self.d * other.d
        result.n = (a.n * b.d) - (b.n * a.d)
        result.d = m
        result.deflate()
        return result

    def __mul__(self, other):
        if type(other) != Fraction:
            other = Fraction(other)
        assert type(other) == Fraction
        result = Fraction()
        result.setn(self.n * other.n)
        result.setd(self.d * other.d)
        result.deflate()
        return result

    def __truediv__(self, other):
        if type(other) != Fraction:
            other = Fraction(other)
        assert type(other) == Fraction
        tempn = other.getd()
        tempd = other.getn()
        tempf = Fraction(tempn, tempd)
        return self * tempf

    def add(self, fraction):
        return self + fraction

    def sub(self, fraction):
        return self - fraction

    def mul(self, other):
        return self * other

    def div(self, other):
        return self / other

    # COMPARISON
    def __eq__(self, other):
        if type(other) != Fraction:
            other = Fraction(other)
        assert type(other) == Fraction
        return self.getn() == other.getn() and self.getd() == other.getd()

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        if type(other) != Fraction:
            other = Fraction(other)
        assert type(other) == Fraction
        a = self.n * other.d
        b = other.n * self.d
        return a > b

    def __lt__(self, other):
        if type(other) != Fraction:
            other = Fraction(other)
        assert type(other) == Fraction
        a = self.n * other.d
        b = other.n * self.d
        return a < b

    def __le__(self, other):
        return not self > other

    def __ge__(self, other):
        return not self < other

    def equals(self, other):
        return self == other

    def notequals(self, other):
        return self != other

    def greater(self, other):
        return self > other

    def greaterorequal(self, other):
        return self >= other

    def less(self, other):
        return self < other

    def lessorequal(self, other):
        return self <= other

    # UNARY
    def __pos__(self):
        return self

    def __neg__(self):
        n = Fraction(1)
        n.n = -self.n
        n.d = self.d
        n.deflate()
        return n

    def __abs__(self):
        self.deflate()
        if self.n < 0:
            return -self
        return self

    # INTERNAL
    @staticmethod
    def gcd(firstint, secondint):
        return math.gcd(firstint, secondint)

    def deflate(self):
        greatestCommonDivisor = self.gcd(self.n, self.d)
        while greatestCommonDivisor != 1:
            self.n = self.n // greatestCommonDivisor
            self.d = self.d // greatestCommonDivisor
            greatestCommonDivisor = self.gcd(self.n, self.d)
        if self.d < 0:
            self.internalMul(-1)
        return

    def internalMul(self, integer):  # multiply both nominator and denominator with same given integer
        assert int(integer) == integer
        assert int(integer) != 0
        self.n = self.n * integer
        self.d = self.d * integer

    def visualInflation(self):  # inflates fraction without loss of nominator floating point precision
        if type(self.n) == float:
            n = len(str(self.n).split(".")[1])
            self.n = int(str(self.n).replace(".", ""))
            self.d = int(self.d * pow(10, n))
