
from charcad.draw.coordinates import Coordinates
from charcad.draw.graph import GraphicObject, GraphicObjectArray, Graph
from charcad.draw.point import Point
from charcad.draw.utils import calc_angle, calc_distance, chrs as ch


class Lines(GraphicObject):
    def __init__(self, x=0, y=0, transparent=True, formatter=None):
        super(Lines, self).__init__(x, y, transparent)
        self.formatter = formatter
        self.objects = GraphicObjectArray()


class Line(Lines):
    def __init__(self, x, y, formatter=None):
        super(Line, self).__init__(x, y, formatter=formatter)

    def __repr__(self):
        return 'Line at <%s>' % id(self)

    def __len__(self):
        return len(self.objects)

    @property
    def origin(self):
        self.coord = Coordinates(self.x, self.y)
        return self.coord

    @property
    def end(self):
        x = self.objects[-1].coord.x
        y = self.objects[-1].coord.y
        self.coord = Coordinates(x, y)
        return self.coord

    @property
    def length(self):
        return len(self)

    def add_point(self, p):
        self.objects.add(p)

    def update_graph(self, w=1, h=1):
        self.graph = Graph(w=w, h=h)
        origin = self.origin
        for obj in self.objects:
            obj.coord -= origin
            self.graph.add_graph(obj)


class Horizontal(Line):
    def __init__(self, x, y, length, marker=None, formatter=None):
        super(Horizontal, self).__init__(x, y, formatter)
        if marker is None:
            marker = ch.lr
        self.marker = marker
        self.create(length)

    def create(self, length):
        for i in range(length):
            p = Point(self.x+i, self.y, marker=self.marker,
                      formatter=self.formatter)
            self.add_point(p)
        self.update_graph(w=length)


class Vertical(Line):
    def __init__(self, x, y, length, marker=None, formatter=None):
        super(Vertical, self).__init__(x, y, formatter)
        if marker is None:
            marker = ch.ud
        self.marker = marker
        self.create(length)

    def create(self, length):
        for i in range(length):
            p = Point(self.x, self.y+i, marker=self.marker,
                      formatter=self.formatter)
            self.add_point(p)
        self.update_graph(h=length)


class Route(Lines):
    def __init__(self, transparent=True):
        super(Route, self).__init__(transparent=transparent)
        self.objects = GraphicObjectArray()

    def __repr__(self):
        return 'Route at <%s>' % id(self)

    def __len__(self):
        return len(self.objects)

    @property
    def origin(self):
        x = min([obj.coord.x for obj in self.objects])
        y = min([obj.coord.y for obj in self.objects])
        return Coordinates(x, y)

    @property
    def h(self):
        return (max([obj.coord.y for obj in self.objects])
                - min([obj.coord.y for obj in self.objects])
                + 1)

    @property
    def w(self):
        return (max([obj.coord.x for obj in self.objects])
                - min([obj.coord.x for obj in self.objects])
                + 1)

    def add_point(self, p):
        self.objects.add(p)

    def create_route(self, *points, marker='.', origin_marker='.',
                     formatter=None, origin_formatter=None):
        for point, next_point in zip(points[0:-1], points[1:]):
            point.set_marker(marker)
            point.set_formatter(formatter)
            self.connect(point, next_point)
        # edit origins
        self.objects[0].set_marker(origin_marker)
        self.objects[0].set_formatter(origin_formatter)
        self.objects[-1].set_marker(origin_marker)
        self.objects[-1].set_formatter(origin_formatter)
        self.coord = self.origin
        self.update()

    def connect(self, p1, p2):
        current_point = p1
        target_point = p2
        arrived = current_point == target_point
        self.add_point(current_point)
        while not arrived:
            next_points = [current_point + m for m in movements]
            distances = [calc_distance(p, target_point)
                         for p in next_points]
            idx = distances.index(min(distances))
            current_point += movements[idx]
            self.add_point(current_point)
            arrived = current_point == target_point

    def update(self):
        self.graph = Graph(w=self.w, h=self.h)
        origin = self.origin
        for obj in self.objects:
            obj.coord -= origin
            self.graph.add_graph(obj)


movements = [
    Coordinates(0, 1),
    Coordinates(1, 1),
    Coordinates(1, 0),
    Coordinates(1, -1),
    Coordinates(0, -1),
    Coordinates(-1, -1),
    Coordinates(-1, 0),
    Coordinates(-1, 1),
]
