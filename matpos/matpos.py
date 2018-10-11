# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from func_helper import pip, mapping, reducing
from .subgrid import Subgrid


class MatPos:
    """
    Store information of:
        1. Store and update size of staging area of subplots
        2. Compute relative position of the new subplot to
            the former subplot
    """

    def __init__(self):
        """
        Generate instance.


        """
        self.origin = (0, 0)
        self.left_top = (0, 0)
        self.right_bottom = (0, 0)
        self.default_figure_style = {
            "facecolor": "white"
        }

    def get_padding(self, padding):
        """
        Reset padding.

        Parameters
        ----------
        padding: dict, optional
            Defining size of padding around all subplots.
            The unit of size is inches.
            Padding of top, left, bottom, and right can be set.
            Default is {
                "top" : 0.1,
                "left" : 0.5,
                "bottom" : 0.5,
                "right" : 0.2
            }
        """
        _padding = {
            "top": 0.1,
            "left": 0.5,
            "bottom": 0.5,
            "right": 0.2
        }
        return {**_padding, **padding}

    def get_width(self):
        """
        Width of rectangle containing all plot areas of subplots.
        Not containing axis and ticks area of subplots
            and padding area of the figure.
        """
        return self.right_bottom[0] - self.left_top[0]

    def get_height(self):
        """
        Hight of rectangle containing all plot areas of subplots.
        Not containing axis and ticks area of subplots
            and padding area of the figure.
        """
        return self.right_bottom[1] - self.left_top[1]

    def get_size(self):
        """
        Tuple of (Width, Hight) of rectangle containing
            all plot areas of subplots.
        Not containing axis and ticks area of subplots
            and padding area of the figure.
        """
        return (self.get_width(), self.get_height())

    def __expand(self, sg_origin, sg_size):
        """
        Expanding rectangle of plot areas
            if the new subplot over the rectangle.
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
        """
        Layout a new subplot based on the position of
            left-top corner of the former subplot.
        """
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

    def add_right(self, sg, size,  margin=0, offset=(0, 0), **kwd):
        """
        Layout a new subplot on the right side of the
            former subplot.

        Parameters
        ----------
        sg: Subgrid
            An instance of Subgrid.
            The position of the new subplot is calculated
                form the subgrid.
        size: tuple(float)
            (width, height) of plot area of the new subplot.
        margin: float, optional
            Distance between the former subplot and the new
                one.
            Default value is 0.
        offset: tuple(float), optional
            (horizontal, vertical) offset from the relative
                origin of the new subplot.
            If you want to adjust margin between 2 subplots,
                please use margin parameter.
            Default velue is (0,0)
        """
        d = margin[0] if type(margin) is tuple else margin

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

    def add_bottom(self, sg, size,  margin=0, offset=(0, 0), **kwd):

        d = margin[1] if type(margin) is tuple else margin

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

    def add_top(self, sg, size,  margin=0, offset=(0, 0), **kwd):
        d = margin[1] if type(margin) is tuple else margin
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

    def add_left(self, sg, size,  margin=0, offset=(0, 0), **kwd):
        d = margin[0] if type(margin) is tuple else margin
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

    def add_grid(self, sizes, column=1, margin=(0, 0), **kwd):
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

        d = margin if type(margin) is tuple else (margin, margin)

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

        return reducing(reducer)([a])(rest_sizes)

    def __scale(self, v, padding={}):
        """
        Scaling position in figure by figure size.
        Padding is took into considered.
        """
        pad = self.get_padding(padding)

        size = np.add(self.get_size(), (pad["left"]+pad["right"], pad["top"] + pad["bottom"])
                      )

        if 0 in size:
            raise SystemError("Size cannot be zero")

        origin = np.add(
            self.left_top, (-pad["left"], -pad["top"]))
        # r = (v - o)/s
        return tuple(
            np.divide(np.add(v, np.multiply(origin, -1)), size)
        )

    def relative(self, subgrid, padding={}):
        """
        Return scaled position of left-top and right-bottom
            corners of a subgrid.
        """

        rel_left_top = self.__scale(subgrid.get_left_top(), padding)
        rel_right_bottom = self.__scale(subgrid.get_right_bottom(), padding)
        return (rel_left_top, rel_right_bottom)

    def axes_position(self, subgrid, padding={}):
        """
        Return matplotlib style position of ax.
        """
        lt, rb = self.relative(subgrid, padding)
        position = [lt[0], 1 - rb[1], rb[0] - lt[0], rb[1] - lt[1]]
        return position

    def generate_axes(self, figure, padding={}):
        """
        Generate matplotlib.pyplot.axsubplot.

        Parameter
        ---------
        figure: matplotlib.pyplot.figure

            Returns
            -------
            ax: matplotlib.pyplot.axsubplot
        """
        def f(subgrid):
            ax = figure.add_subplot(
                111,
                position=self.axes_position(subgrid, padding),
                **subgrid.get_axes_kwargs(),
                **subgrid.get_shared_axis()
            )
            subgrid.set_ax(ax)
            return ax
        return f

    def figure_and_axes(self, subgrids, padding={}, figsize=None, **kwargs):
        """
        Generate matplotlib.pyplot.figure and its subplots of
            matplotlib.pyplot.axsubplot.

        This method also takes key word arguments same with matplotlib.pyplot.figure.

        Paraeters
        ---------
        subgrids: list[Subgrid]
            List of Subgrids generated by this instance.
        padding: dict, optional
            Dictionary to overwrite default padding size around plot areas of subplots.
            It can have keys "top", "left", "bottom", and "right.
            If padding are too small, axises may be out of image.
            Default value is empty dictionaly.
        figsize: tuple(float), optional
            Tuple with 2 float number (width, height) to overwrite figure size.
            Default value is None.
        kwargs:
            Key word arguments compatible to matplotlib.pyplot.figure.

        Return
        ------
        fig: matplotlib.figure.Figure
        axs: list[matplotlib.axes._subplots.AxesSubplot]
        """

        fig = plt.figure(
                figsize=self.get_size() if figsize is None else figsize,
                **dict(self.default_figure_style, **kwargs)
            )
        axs = pip(
            mapping(self.generate_axes(fig, padding)),
            list
        )(subgrids)

        return(fig, axs)

    @staticmethod
    def fontsize_to_inch(fontsize, n):
        """
        Assist determin padding size when font size
            and number of characters are given.

        Parameters
        ----------
        fontsize: float
            Unit is px.
        n: float
            Number of characters.

        Return
        ------
        padding: float
            Unit of inches

        Usage
        -----
        padding = MatPos.fontsize_to_point(12, 5)

        """
        return fontsize*n/72
