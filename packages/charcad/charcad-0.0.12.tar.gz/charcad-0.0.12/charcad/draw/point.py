from numbers import Number as numeric
from charcad.draw.coordinates import Coordinates
from charcad.draw.graph import GraphicObject, Graph
from charcad.draw.utils import Formatter


class Point(GraphicObject):
    def __init__(self, x=0, y=0, marker='.', formatter=None):
        if isinstance(y, str):
            marker = y
            y = None
        super().__init__(x, y)
        if not isinstance(marker, str):
            raise TypeError("marker should be str.")
        self.marker = marker[0]
        self.set_formatter(formatter)

    def __add__(self, other):
        if isinstance(other, Point):
            new_point = Point(self.coord + other.coord, marker=self.marker,
                              formatter=self.formatter)
        elif isinstance(other, (Coordinates, tuple)):
            new_point = Point(self.coord + other, marker=self.marker,
                              formatter=self.formatter)
        else:
            raise TypeError("'other' must be a Point or a Coordinates object.")
        return new_point

    def __sub__(self, other):
        if isinstance(other, Point):
            new_point = Point(self.coord - other.coord, marker=self.marker,
                              formatter=self.formatter)
        elif isinstance(other, (Coordinates, tuple)):
            new_point = Point(self.coord - other, marker=self.marker,
                              formatter=self.formatter)
        else:
            raise TypeError("'other' must be a Point or a Coordinates object.")
        return new_point

    def __mul__(self, other):
        if isinstance(other, numeric):
            return Point(self.coord*other, marker=self.marker,
                         formatter=self.formatter)
        else:
            raise TypeError("'other' must be numeric.")

    def __truediv__(self, other):
        if isinstance(other, numeric):
            return Point(self.coord/other, marker=self.marker,
                         formatter=self.formatter)
        else:
            raise TypeError("'other' must be numeric.")

    def __eq__(self, other):
        if isinstance(other, Point):
            eq = self.coord == other.coord
        elif isinstance(other, Coordinates):
            eq = self.coord == other
        else:
            eq = False
        return eq

    def __getitem__(self, item):
        return self.coord[item]

    def __repr__(self):
        return 'Point({}, {}, {})'.format(self.x, self.y, self.marker)

    def __floor__(self):
        return Point(int(self.coord), marker=self.marker,
                     formatter=self.formatter)

    def __round__(self, n=0):
        return Point(round(self.coord, n), marker=self.marker,
                     formatter=self.formatter)

    def set_formatter(self, formatter):
        if formatter is None:
            formatter = Formatter()
        self.formatter = formatter
        self.set_marker(self.marker)

    def set_marker(self, marker):
        self.marker = marker[0]
        self.graph = Graph(self.formatter.format(self.marker))
