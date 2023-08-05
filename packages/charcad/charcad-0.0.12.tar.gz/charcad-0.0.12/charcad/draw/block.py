from charcad.draw.coordinates import Coordinates
from charcad.draw.canvas import Canvas
from charcad.draw.graph import add_frame


class Block(Canvas):
    def __init__(self, w, h, x=0, y=0, framed=True, frame_formatter=None):
        super(Block, self).__init__(w=w, h=h)
        self.framed = framed
        self.set_frame_formatter(frame_formatter)
        self.coord = Coordinates(x, y)

    def _add_frame(self):
        self.graph = add_frame(self.graph, formatter=self.frame_formatter)

    def show(self, axes=False):
        self.update()
        self.graph.print(axes=axes, frame=False)

    def set_frame_formatter(self, formatter):
        self.frame_formatter = formatter
        self.update()
    
    def update(self):
        self.reset_graph()
        if self.framed:
            self._add_frame()
        self.graph.add_objects(self.objects)
