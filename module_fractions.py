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

"""
Class Description:
This class implements simple fractions, based on python's int data type. 
At all times, both the nominator and denominator should be of type int to the outside world.
Floating point numbers and other fractions are not supported internally. However, it is possible to generate a fraction 
by providing a float type nominator to the constructor. The denominator has to be an int type number.
The following methods are implemented:

(EXTERNAL METHODS)
Fraction(nominator*, denominator*) -> constructor, creates Fraction based on given number(s)
- nominator: optional int or float, default is 0
- denominator: optional int, default is 1, cannot be equal 0
getn() -> returns current nominator
getd() -> return current denominator
setn(nominator) -> sets nominator to new int type number
setn(denominator) -> sets denominator to new int type number
print() -> prints a visual representation of the fraction
getApproximation() -> returns a float type numerical approximation of the fraction (ATTENTION: IMPRECISE!) 

(ARITHMETIC OPERATORS)
__add__(other) -> implements addition, other can be int, float, or Fraction
add(other) -> wrapper for __add__(other) object method
__sub__(other) -> implements subtraction, other can be int, float, or Fraction
sub(other) -> wrapper for __sub__(other) object method
__mul__(other) -> implements multiplication, other can be int, float, or Fraction
mul(other) -> wrapper for __mul__(other) object method
__truediv__(other) -> implements division, other can be int, float, or Fraction
div(other) -> wrapper for __truediv__(other) object method

(COMPARISON OPERATORS)
__eq__(other) -> checks for equality based on the visual representation
equals(other) -> wrapper for __eq__(other) object method

(INTERNAL METHODS)
deflate() -> shortens the fraction so that equality can be determined correctly
internalMul(integer) -> multiplies both the nominator and the denominator with a given int type number
visualInflation() -> inflates floating point nominator in fraction to an int type without loss of precision
__repr__() -> returns visual representation of fraction, also used for equality comparison
"""


class Fraction:
    n = 0  # nominator
    d = 1  # denominator

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

    def deflate(self):
        greatestCommonDivisor = math.gcd(self.n, self.d)
        while greatestCommonDivisor != 1:
            self.n = self.n // greatestCommonDivisor
            self.d = self.d // greatestCommonDivisor
            greatestCommonDivisor = math.gcd(self.n, self.d)
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

    def __repr__(self):
        self.deflate()
        return f"({self.n}/{self.d})"

    def print(self):
        print(self)

    def getApproximation(self):
        return float(self.n / self.d)

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

    def add(self, fraction):
        return self + fraction

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

    def sub(self, fraction):
        return self - fraction

    def __mul__(self, other):
        if type(other) != Fraction:
            other = Fraction(other)
        assert type(other) == Fraction
        result = Fraction()
        result.setn((self.getn() * other.getn()))
        result.setd((self.getd() * other.getd()))
        result.deflate()
        return result

    def mul(self, other):
        return self * other

    def __truediv__(self, other):
        if type(other) != Fraction:
            other = Fraction(other)
        assert type(other) == Fraction
        tempn = other.getd()
        tempd = other.getn()
        tempf = Fraction(tempn, tempd)
        return self * tempf

    def div(self, other):
        return self / other

    def __eq__(self, other):
        return self.__repr__() == other.__repr__()

    def equals(self, other):
        return self == other
