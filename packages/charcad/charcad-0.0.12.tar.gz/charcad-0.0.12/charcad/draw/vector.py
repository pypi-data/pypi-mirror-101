import math
from numbers import Number as numeric

from charcad.draw.coordinates import Coordinates
from charcad.draw.utils import calc_angle


class Vector:
    def __init__(self, *p, origin=Coordinates(0, 0)):
        if isinstance(p[0], tuple):
            p = Coordinates(*p[0])
        elif isinstance(p[0], Coordinates):
            p = p[0]
        elif isinstance(p[0], numeric):
            p = Coordinates(*p)

        if isinstance(origin, tuple):
            origin = Coordinates(*origin)

        self.p = p
        self.origin = origin

    def __abs__(self):
        return math.hypot(*self.p)

    def __add__(self, other):
        return Vector(self.p + other.p, self.origin)

    def __mul__(self, other):
        if isinstance(other, (float, int)):
            return Vector(self.p * other)
        else:
            raise Exception("'other' must be scalar.")

    def __truediv__(self, other):
        if isinstance(other, (float, int)):
            return Vector(self.p / other)
        else:
            raise Exception("'other' must be scalar.")

    def __repr__(self):
        return "vector[{}, {}]".format(self.p, self.origin)

    def angle(self, other=None):
        if other is None:
            other = Vector(1, 0)
        return calc_angle(self, other)

    def dot(self, other):
        return sum([i1 * i2 for i1, i2 in zip(self.p, other.p)])

    @property
    def unit(self):
        return Vector(self.p/abs(self))
