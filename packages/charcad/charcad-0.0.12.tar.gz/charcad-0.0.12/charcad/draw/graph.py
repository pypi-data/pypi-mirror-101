import math
import numpy as np
from copy import deepcopy

from charcad.draw.coordinates import Coordinates
from charcad.draw.utils import DrawingChars


_EMPTY_GRID = np.array([[' ']])


class GraphicObject:
    def __init__(self, x=0, y=0, transparent=True):
        self.set_coordinates(x, y)
        self.graph = None
        self.set_transparency(transparent)

    @property
    def x(self):
        return self.coord.x

    @property
    def y(self):
        return self.coord.y

    def set_coordinates(self, x, y=None):
        if isinstance(x, Coordinates):
            coord = x
        elif isinstance(x, (list, tuple)):
            coord = Coordinates(*x)
        else:
            coord = Coordinates(x, y)
        self.coord = coord

    def set_transparency(self, transparent):
        self.transparent = transparent

    def set_x(self, x):
        self.coord.x = x

    def set_y(self, y):
        self.coord.y = y

    def show(self, axes=False, frame=False, frame_formatter=None):
        self.graph.print(axes=axes, frame=frame,
                         frame_formatter=frame_formatter)


class GraphicObjectArray:
    def __init__(self):
        self._objects = dict()
        self._counter = 0

    def __getitem__(self, key):
        if isinstance(key, str):
            self._objects[key]
        else:
            key_aux = self.keys
            key_aux.sort()
            if isinstance(key, slice):
                item = [self._objects[k] for k in key_aux[key]]
            else:
                item = self._objects[key_aux[key]]
        return item

    def __len__(self):
        return len(self._objects)

    def __repr__(self):
        z = zip(self.keys, self.values)
        p = int(math.log10(len(self)) + 1)
        return 'Graphic Object Array[\n  %s\n]' % ',\n  '\
            .join([(str(i).zfill(p) + '\t' + k + ': %s') % v
                   for i, (k, v) in enumerate(z)])

    @property
    def keys(self):
        return list(self._objects.keys())

    @property
    def values(self):
        return list(self._objects.values())

    def add(self, obj):
        name = 'object_{:04d}'.format(self._counter)
        self._check_duplicates(obj)
        self._objects.update({name: obj})
        self._counter += 1

    def _check_duplicates(self, obj):
        [delete_object(o) for o in self if obj == o]

    def remove(self, key):
        if isinstance(key, (list, tuple)):
            key = list(key)
            key.sort(reverse=True)
            [self.remove(k) for k in key]
        else:
            if isinstance(key, str):
                pass
            elif isinstance(key, int):
                key = self.keys[key]
            else:
                raise TypeError("key must be integer, string or iterable.")
            del self._objects[key]

    def update(self, item):
        self._objects.update(item)


class Graph:
    def __init__(self, grid=None, w=0, h=0):
        if grid is None:
            grid = np.full((h, w), ' ', dtype=object)
        elif isinstance(grid, str):
            grid = np.array([[grid]])
        elif isinstance(grid, np.ndarray):
            pass
        else:
            raise TypeError('grid cant be numeric.')
        self.grid = grid

    def __repr__(self):
        return self.get_str()

    def __len__(self):
        return len(self.grid)

    def __getitem__(self, key):
        return Graph(self.grid[key])

    def __setitem__(self, key, value):
        # i utterly hate this
        key = list(key)
        for i, k in enumerate(key):
            if not isinstance(k, slice):
                key[i] = slice(k, k+1)
        key = tuple(key)
        self.grid[key] = value.grid

    @property
    def h(self):
        return self.grid.shape[0]

    @property
    def w(self):
        return self.grid.shape[1]

    @property
    def shape(self):
        return (self.h, self.w)

    def add_objects(self, graphicArray):
        for obj in graphicArray:
            if isinstance(obj, GraphicObjectArray):
                self.add_objects(obj)
            elif isinstance(obj, GraphicObject):
                self.add_graph(obj)
            else:
                raise TypeError(
                    "obj must be GraphicObject or GraphicObjectArray.")

    def add_graph(self, obj, x=0, y=0):
        if isinstance(x, Coordinates):
            coord_other = x
        else:
            coord_other = Coordinates(x, y)
        coord = obj.coord + coord_other
        xi = coord.x
        xf = coord.x + obj.graph.w
        yf = self.flipud(coord.y - 1)
        yi = self.flipud(coord.y - 1 + obj.graph.h)
        x_slice = slice(xi, xf)
        y_slice = slice(yi, yf)
        transparent = obj.transparent
        if transparent:
            new_subgraph = self[y_slice, x_slice].no_background_draw(obj.graph)
        else:
            new_subgraph = obj.graph
        self[y_slice, x_slice] = new_subgraph

    def copy(self):
        grid = self.grid.copy()
        return Graph(grid=grid)

    def flipud(self, yi):
        return self.h - yi - 1

    def get_str(self):
        return '\n'.join([''.join(row) for row in self.grid])

    def inspect(self):
        [print(item) for item in [row for row in self.grid]]

    def isempty(self):
        return self.grid == _EMPTY_GRID

    def no_background_draw(self, other, rng=None):
        gph_out = self.copy()
        for i in range(self.h):
            for j in range(self.w):
                iother = other[i, j]
                if not iother.isempty():
                    gph_out[i, j] = iother[0, 0]
        return gph_out

    def print(self, frame=False, axes=False, frame_formatter=None):
        grph = deepcopy(self)
        if frame:
            grph = add_frame(grph, frame_formatter)
        if axes:
            grph = add_axes(grph, self.w, self.h)
        print(grph)


def add_axes(grph, w, h):
    # axis order of gratness
    yg = int(math.log10(grph.h) + 1)
    xg = int(math.log10(grph.w) + 1)
    # check offset (caused by frame)
    offset_h = int((grph.h - h) / 2)
    offset_w = int((grph.w - w) / 2)
    # y axis (with frame and axis compensation)
    yaxis = (
        [' ' * yg] * offset_h
        + [str(h - y - 1).zfill(yg) for y in range(h)]
        + [' ' * yg] * offset_h
    )
    # x axis (with frame and axis compensation)
    xaxis = list()
    for i in range(xg):
        n = 10**i
        xaxis.append(
            [' ' * yg]
            + [' '] * offset_w
            + [str(int(x/n) % 10) if (x % n) == 0
               else ' ' for x in range(w)]
            + [' '] * offset_w
        )
    # add to original grid
    grph.grid = np.c_[yaxis, grph.grid]
    grph.grid = np.r_[grph.grid, xaxis]
    return grph


def add_frame(grph, formatter=None):
    chrs = DrawingChars()
    if formatter is not None:
        [chrs.__dict__.update({k: formatter.format(ch)})
         for k, ch in chrs.__dict__.items()]
    li = [[chrs.ur] + grph.w * [chrs.lr] + [chrs.rd]]
    lf = [[chrs.dr] + grph.w * [chrs.lr] + [chrs.ru]]
    grph.grid = np.c_[[chrs.ud] * grph.h, grph.grid, [chrs.ud] * grph.h]
    grph.grid = np.r_[li, grph.grid, lf]
    return grph


def delete_object(obj):
    del obj
