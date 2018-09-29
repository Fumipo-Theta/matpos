# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from func_helper import pip, mapping, reducing


class Subgrid:
    def __init__(self, size, origin, sharex=None, sharey=None, **kwd):
        if size[0] < 0 or size[1] < 0:
            raise SystemError("size must be positive")
        self.size = size
        self.origin = origin
        self.set_shared_axis(sharex, sharey)
        self.axes_kwargs = kwd

    def get_left_top(self):
        return self.origin

    def get_right_bottom(self):
        return tuple(np.add(self.origin, self.size))

    def get_width(self):
        return self.size[0]

    def get_height(self):
        return self.size[1]

    def get_size(self):
        return self.size

    def set_ax(self, ax):
        self.ax = ax

    def get_ax(self):
        return self.ax

    def set_shared_axis(self, sharex=None, sharey=None):
        self.sharex = sharex
        self.sharey = sharey

    def get_shared_axis(self):
        return {
            "sharex": self.sharex.get_ax() if type(self.sharex) is Subgrid else None,
            "sharey": self.sharey.get_ax() if type(self.sharey) is Subgrid else None
        }

    def set_axes_kwargs(self, **kwd):
        self.axes_kwargs = kwd

    def get_axes_kwargs(self):
        return self.axes_kwargs


class EmptyGrid(Subgrid):
    def __init__(self, size, origin):
        super(size, origin)


class MatPos:
    """
    Subgridを追加するたび, Figureの左上と右下の座標を更新していくことにより,
        後にSubgridのFigure上での相対座標を計算を可能にするクラス.
    Figureの座標は, 追加されるSubgridのサイズに基づいて決まるので,
        SubgridのサイズをFigure全体のサイズから逆算する必要がなく,
        直接指定することができる.
    Subgridは最初の一つはFigureの原点を基準として追加されるが,
        2つ目以降はすでに位置とサイズを指定したSubgridを基準として
        配置することができる.
    """

    def __init__(self, padding={
        "left": 0.5,
        "right": 0.2,
        "top": 0.1,
        "bottom": 0.5
    }):
        self.origin = (0, 0)
        self.padding = {"left": 0, "right": 0, "top": 0, "bottom": 0}

        self.set_padding(padding)
        self.left_top = (0, 0)
        self.right_bottom = (0, 0)

    def set_padding(self, padding):

        self.padding["left"] = padding.get("left", 0)
        self.padding["right"] = padding.get("right", 0)
        self.padding["top"] = padding.get("top", 0)
        self.padding["bottom"] = padding.get("bottom", 0)

    def get_width(self):
        return self.right_bottom[0] - self.left_top[0]

    def get_height(self):
        return self.right_bottom[1] - self.left_top[1]

    def get_size(self):
        return (self.get_width(), self.get_height())

    def __expand(self, sg_origin, sg_size):
        """
        追加したSubgridがGridFigureの領域をはみ出す場合は,
            GridFigureの領域を拡大する.
        """
        self.left_top = (
            np.min([self.left_top[0], sg_origin[0]]),
            np.min([self.left_top[1], sg_origin[1]])
        )

        self.right_bottom = (
            np.max([self.right_bottom[0], sg_origin[0] + sg_size[0]]),
            np.max([self.right_bottom[1], sg_origin[1] + sg_size[1]])
        )

    def from_left_top(self, sg, size, offset=(0, 0), **kwd):
        next_origin = (
            sg.origin[0] + offset[0],
            sg.origin[1] + offset[1]
        )

        next_size = (
            size[0] if size[0] is not None else sg.get_width() - offset[0],
            size[1] if size[1] is not None else sg.get_height() - offset[1]
        )

        self.__expand(next_origin, next_size)
        return Subgrid(next_size, next_origin,  **kwd)

    def from_left_bottom(self, sg, size, offset=(0, 0),  **kwd):

        next_size = (
            size[0] if size[0] is not None else sg.get_width() - offset[0],
            size[1] if size[1] is not None else sg.get_height() - offset[1]
        )

        next_origin = (
            sg.origin[0] + offset[0],
            sg.origin[1] + sg.size[1] - offset[1] - next_size[1]
        )

        self.__expand(next_origin, next_size)
        return Subgrid(next_size, next_origin,  **kwd)

    def from_right_top(self, sg, size, offset=(0, 0),  **kwd):
        next_size = (
            size[0] if size[0] is not None else sg.get_width() - offset[0],
            size[1] if size[1] is not None else sg.get_height() - offset[1]
        )

        next_origin = (
            sg.origin[0] + sg.size[0] - offset[0] - next_size[0],
            sg.origin[1] + offset[1]
        )

        self.__expand(next_origin, next_size)
        return Subgrid(next_size, next_origin, **kwd)

    def from_right_bottom(self, sg, size, offset=(0, 0), **kwd):
        next_size = (
            size[0] if size[0] is not None else sg.get_width() - offset[0],
            size[1] if size[1] is not None else sg.get_height() - offset[1]
        )

        next_origin = (
            sg.origin[0] + sg.get_width() - offset[0] - next_size[0],
            sg.origin[1] + sg.get_height() - offset[1] - next_size[1]
        )

        self.__expand(next_origin, next_size)
        return Subgrid(next_size, next_origin, **kwd)

    def add_right(self, sg, size,  distance=0, offset=(0, 0), **kwd):

        d = distance[0] if type(distance) is tuple else distance

        next_origin = (
            sg.origin[0] + sg.get_width() + d + offset[0],
            sg.origin[1] + offset[1]
        )

        next_size = (
            size[0],
            size[1] if size[1] is not None else self.get_height() -
            next_origin[1]
        )

        self.__expand(next_origin, next_size)
        return Subgrid(next_size, next_origin, **kwd)

    def add_bottom(self, sg, size,  distance=0, offset=(0, 0), **kwd):

        d = distance[1] if type(distance) is tuple else distance

        next_origin = (
            sg.origin[0] + offset[0],
            sg.origin[1] + sg.get_height() + d + offset[1]
        )

        next_size = (
            size[0] if size[0] is not None else self.get_width() -
            next_origin[0],
            size[1]
        )

        self.__expand(next_origin, next_size)
        return Subgrid(next_size, next_origin, **kwd)

    def add_top(self, sg, size,  distance=0, offset=(0, 0), **kwd):
        d = distance[1] if type(distance) is tuple else distance
        next_origin = (
            sg.origin[0] + offset[0],
            sg.origin[1] - size[1] - d - offset[1]
        )

        next_size = (
            size[0] if size[0] is not None else self.get_width() -
            next_origin[0],
            size[1]
        )

        self.__expand(next_origin, next_size)
        return Subgrid(next_size, next_origin, **kwd)

    def add_left(self, sg, size,  distance=0, offset=(0, 0), **kwd):
        d = distance[0] if type(distance) is tuple else distance
        next_origin = (
            sg.origin[0] - offset[0] - d - size[0],
            sg.origin[1] + offset[1]
        )

        next_size = (
            size[0],
            size[1] if size[1] is not None else self.get_height() -
            next_origin[1]
        )

        self.__expand(next_origin, next_size)
        return Subgrid(next_size, next_origin, **kwd)

    def add_grid(self, sizes, column=1, distance=(0, 0), **kwd):
        """
        Generates subgrids aligning as grid layout.
        Order of subgrid is column prefered.

        Parameters
        ----------
        sizes: List[Tuple[float]]
            List of tuples which have 2 float numbers.
            The tuple defines width and height (w, h) of
                a subplot by unit of inches.

        column: int, optional
            Number of columns in grid.
            Default value is 1.

        offset: Tuple[float], optional
            Offsets between subgrids.
            It has 2 float numbers indicating horizontal and vertical
                distances (h, v) between subgrids.
            Default value is (0, 0).

        Return
        ------
        subgrids: List[Subgrid]
            List of instances of Subgrid class.
            The length is equal to that of sizes parameter.

        Example
        -------
        # Generate 3 x 3 grid from 9 subplots whose plot area sizes are 3 x 3.

        gridder = Gridder()

        subgrids = gridder.add_grid(
            [(3,3) for i in range(9)],
            3,
            offset=(0.5, 0.5)
        )

        """

        d = distance if type(distance) is tuple else (distance, distance)

        size, *rest_sizes = sizes
        a = self.from_left_top(self, size)

        def reducer(acc, e):
            l = len(acc)
            if l % column is 0:
                newSg = self.add_bottom(
                    acc[l-column], e, d, **kwd)
            else:
                newSg = self.add_right(acc[l-1], e, d, **kwd)
            return [*acc, newSg]

        return reducing(reducer)(rest_sizes)([a])

    def __scale(self, v):
        size = np.add(self.get_size(), (self.padding["left"]+self.padding["right"], self.padding["top"] + self.padding["bottom"])
                      )

        if 0 in size:
            raise SystemError("Size cannot be zero")

        origin = np.add(
            self.left_top, (-self.padding["left"], -self.padding["top"]))
        # r = (v - o)/s
        return tuple(
            np.divide(np.add(v, np.multiply(origin, -1)), size)
        )

    def relative(self, subgrid):
        rel_left_top = self.__scale(subgrid.get_left_top())
        rel_right_bottom = self.__scale(subgrid.get_right_bottom())
        return (rel_left_top, rel_right_bottom)

    def axes_position(self, subgrid):
        lt, rb = self.relative(subgrid)
        position = [lt[0], 1 - rb[1], rb[0] - lt[0], rb[1] - lt[1]]
        return position

    def generate_axes(self, figure):
        def f(subgrid):
            ax = figure.add_subplot(
                111,
                position=self.axes_position(subgrid),
                **subgrid.get_axes_kwargs(),
                **subgrid.get_shared_axis()
            )
            subgrid.set_ax(ax)
            return ax
        return f

    def figure_and_axes(self, subgrids, figsize=None):
        fig = plt.figure(figsize=self.get_size()
                         if figsize is None else figsize)
        axes = pip(
            mapping(self.generate_axes(fig)),
            list
        )(subgrids)

        return(fig, axes)
