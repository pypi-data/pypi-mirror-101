from charcad.draw.graph import Graph, GraphicObject, GraphicObjectArray
from charcad.draw.point import Point
from charcad.draw.coordinates import Coordinates


class Text(GraphicObject):
    def __init__(self, x=0, y=0, transparent=True, formatter=None,
                 alignment='center', text=None):
        super(Text, self).__init__(x, y, transparent)
        self.formatter = formatter
        self.objects = GraphicObjectArray()
        self.alignment = alignment
        if text is not None:
            self.write(text)

    @property
    def origin(self):
        self.coord = Coordinates(self.x, self.y)
        return self.coord

    def add_point(self, p):
        self.objects.add(p)

    def align(self, alignment=None):
        def calc_offset(w, sz):
            if self.alignment == 'center':
                return int((w - sz)/2)
            elif self.alignment == 'right':
                return w - sz
            elif self.alignment == 'left':
                return 0
        if alignment is None:
            alignment = self.alignment
        else:
            self.alignment = alignment
        w = self.w
        h = self.h
        objects_list = [
            [obj for obj in self.objects if obj.y == i]
            for i in range(h)]
        for lst in objects_list:
            x0 = lst[0].x
            sz = len(lst)
            offset = calc_offset(w, sz) - x0
            for obj in lst:
                obj.coord.x += offset
        self.update_graph()

    def format_text(self, formatter=None):
        if formatter is not None:
            self.formatter = formatter
        for obj in self.objects:
            obj.set_formatter(self.formatter)
        self.update_graph()

    def update_graph(self):
        self.graph = Graph(w=self.w, h=self.h)
        for obj in self.objects:
            self.graph.add_graph(obj)

    def write(self, text):
        if isinstance(text, (list, tuple)):
            w = max([len(t) for t in text])
            h = len(text)
            self.set_y(self.y - (h-1))
            for j, txt in enumerate(text):
                j_ = (h-1) - j
                for i, t in enumerate(txt):
                    p = Point(i, j_, marker=t)
                    self.add_point(p)
        elif isinstance(text, str):
            w = len(text)
            h = 1
            for i, t in enumerate(text):
                p = Point(i, 0, marker=t)
                self.add_point(p)
        else:
            raise TypeError("'text' must be s string or a list of strings")
        self.w = w
        self.h = h
        self.format_text()
        self.align()
