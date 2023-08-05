# canvas module

from charcad.draw.graph import GraphicObject, GraphicObjectArray, Graph
from charcad.draw.point import Point
from charcad.draw.lines import Route, Horizontal, Vertical
from charcad.draw.text import Text


class Canvas(GraphicObject):
    def __init__(self, w, h):
        super(Canvas, self).__init__()
        self.draw = Draw(self)
        self.w = w
        self.h = h
        self.reset()

    def add_object(self, obj, x=None, y=None, coord=None):
        if not coord is None:
            obj.set_coordinates(coord)
        elif x is not None and y is not None:
            obj.set_coordinates(x, y)
        self.objects.add(obj)

    def remove_object(self, key):
        self.objects.remove(key)

    def reset(self):
        self.objects = GraphicObjectArray()
        self.reset_graph()

    def reset_graph(self):
        self.graph = Graph(w=self.w, h=self.h)

    def show(self, axes=False, frame=False, frame_formatter=None):
        self.update_graph()
        self.graph.print(axes=axes, frame=frame,
                         frame_formatter=frame_formatter)

    def undo(self):
        self.objects.remove(-1)

    def update_graph(self):
        self.reset_graph()
        for obj in self.objects:
            try:
                obj.update()
            except:
                pass
        self.graph.add_objects(self.objects)


class Draw:
    def __init__(self, outer):
        self._canvas = outer
        self.line = self._Line(outer)

    def point(self, p, formatter=None):
        if isinstance(p, (list, tuple)):
            p = Point(*p)
            p.set_formatter(formatter)
        self._canvas.add_object(p)

    def text(self, text, x=0, y=0, transparent=True, formatter=None,
             alignment='center'):
        txt = Text(x, y, text=text, transparent=transparent,
                   formatter=formatter, alignment=alignment)
        self._canvas.add_object(txt)

    class _Line:
        def __init__(self, outer):
            self._canvas = outer

        def __call__(self, direction, *a, **kw):
            if direction.lower() in ['h', 'horizontal']:
                self.horizontal(*a, **kw)
            elif direction.lower() in ['v', 'vertical']:
                self.vertical(*a, **kw)
            else:
                raise Exception(
                    "'%s' is an invalid direction." % direction)

        def horizontal(self, x, y, length, marker=None, formatter=None):
            line = Horizontal(x, y, length, marker=marker, formatter=formatter)
            line.formatter = formatter
            self._canvas.add_object(line)

        def vertical(self, x, y, length, marker=None, formatter=None):
            line = Vertical(x, y, length, marker=marker, formatter=formatter)
            line.formatter = formatter
            self._canvas.add_object(line)

        def route(self, *p, marker='.', origin_marker=None,
                  formatter=None, origin_formatter=None, transparent=True):
            if origin_marker is None:
                origin_marker = marker
            p = list(p)
            for i, item in enumerate(p):
                if isinstance(item, (tuple, list)):
                    p[i] = Point(*item)
                elif isinstance(item, Point):
                    p[i] = item
            route = Route(transparent=transparent)
            route.create_route(*p, marker=marker, origin_marker=origin_marker,
                               formatter=formatter,
                               origin_formatter=origin_formatter)
            self._canvas.add_object(route)
