from numbers import Number as numeric


class Coordinates:
    def __init__(self, x=0, y=0):
        self.x = int(x)
        self.y = int(y)

    def __add__(self, other):
        return Coordinates(self.x + other[0], self.y + other[1])

    def __sub__(self, other):
        return Coordinates(self.x - other[0], self.y - other[1])

    def __mul__(self, other):
        if isinstance(other, numeric):
            return Coordinates(self.x*other, self.y*other)
        else:
            raise TypeError("'other' must be numeric.")

    def __truediv__(self, other):
        if isinstance(other, numeric):
            return Coordinates(self.x/other, self.y/other)
        else:
            raise TypeError("'other' must be numeric.")

    def __eq__(self, other):
        return (self.x == other.x) & (self.y == other.y)

    def __getitem__(self, item):
        return [self.x, self.y][item]

    def __repr__(self):
        return 'Coordinates({}, {})'.format(self.x, self.y)

    def __floor__(self):
        return Coordinates(int(self.x), int(self.y))

    def __round__(self, n=0):
        return Coordinates(round(self.x, n), round(self.y, n))
