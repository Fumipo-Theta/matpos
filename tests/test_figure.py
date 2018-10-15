# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.3'
#       jupytext_version: 0.8.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
#   language_info:
#     codemirror_mode:
#       name: ipython
#       version: 3
#     file_extension: .py
#     mimetype: text/x-python
#     name: python
#     nbconvert_exporter: python
#     pygments_lexer: ipython3
#     version: 3.7.0
# ---

# +

from matdat import Figure, Subplot, SubplotTime
from matdat import linePlot, scatterPlot
from matpos import MatPos
import matplotlib.pyplot as plt

# %matplotlib inline
# -

f = plt.figure(figsize=(8,6))
a = f.add_subplot(111,position=[0.3,0.3, 0.2,0.2])
a.plot([0,1],[0,1])
b = f.add_subplot(111,position=[0.5,0.5, 0.5,0.5], sharex=a)
a.set_xlim([0,2])

# +
mp = MatPos()

outer = mp.from_left_top(mp, (5,5))
lt = mp.from_left_top(outer, (2,2), (0.5,0.5))
lb = mp.from_left_bottom(outer, (1,1), (0.5,0.5))
rt = mp.from_right_top(outer, (1,1), (0.5,0.5))
rb = mp.from_right_bottom(outer, (2,2), (0.5,0.5))

fig, axs = mp.figure_and_axes([outer, lt, lb, rt, rb]
                              ,padding={"left":1, "right":1, "top":1,"bottom":1}
                              )
print(fig,axs)
axs[0].text(0.05,0.95, "outer")
axs[1].text(0.5,0.5,"lt")
axs[2].text(0.5,0.5,"lb")
axs[3].text(0.5,0.5,"rt")
axs[4].text(0.5,0.5,"rb")
# -

ax = axs[0]
ax?

# +
figure=Figure()

subplot=Subplot.create() \
    .register(
        data = {"x":[0,1,2], "y":[0,1,4]},
        option = {"x" : "x", "y" : "y", "xLabel": "$X$", "yLabel" : "$Y$"},
        plot = [linePlot()],
        limit = {"xlim" : [0,10]}
    ) \
    .register(
        data = {"x":[0,1,2,3,4], "y":[0,0.5,1,1.5,2]},
        option = {"x" : "x", "y" : "y", "xLabel": "$X$", "yLabel" : "$Y$", "ylim" : [0,4]},
        plot = [scatterPlot()]
    )

figure.add_subplot(subplot,"a")

figure.add_subplot(
    Subplot.create()
        .register(
        data = {"x":[0,1,2], "y":[0,1,4]},
        option = {"x" : "x", "y" : "y"},
        plot = [scatterPlot({"s":10, "color" : "red"})]
    ),
    "b"
)

figure.add_subplot(
    Subplot.create()
        .register(
        data = {"x":[0,1,2], "y":[0,1,4]},
        option = {"x" : "x", "y" : "y"},
        plot = [linePlot(), scatterPlot({"s":100, "color" : "red"})]
    ),
    "c"
)

fig, ax = figure.show(size=[(4,3) for i in range(figure.get_length())], column=2, margin=(1,2),test=False)


#print(ax)
#xtick = ax[0].get_xticks()
#ax[0].set_xticklabels(xtick)

# +
# Same size grid plot
fig, ax = figure.show(size=(4,3), column=2, margin=(1,2), padding={},test=False, facecolor="gray")
print(ax)

# Different size grid mode
fig, ax = figure.show(size=[(4,3) for i in range(figure.get_length())], column=2, margin=(1,1), padding={},test=False)

# Use setting dictionary 
figure_size_setting = {"size":(4,3), "column":2, "margin":(1,2), "padding":{}}
fig, ax = figure.show(figure_size_setting,test=False, facecolor="gray")

# Custom layout mode
mp = MatPos()
a = mp.from_left_top(mp, (2,2))
b = mp.add_bottom(a, (2,1), margin=1)
c = mp.add_right(a, (2,None), margin=1)

fig, ax = figure.show(mp, [a,b,c])
# -

Figure?

# +
matpos = MatPos()
a = matpos.add_right(matpos,(4,3))
c = matpos.add_bottom(a, (4,3), margin=1, sharex=a)
b = matpos.add_right(a, (4, None), margin=1)

fig, ax = figure.show_custom(matpos, [a,b,c])
ax["a"].grid(True)

# +
print(
    
    tuple(np.add((1,2),np.multiply((3,4),-1))),
    0 in (0,1,1),
    0.0 in (0,1,1),
    0 in (0.0,1,1)
    
)

a, *b = [1,2,3]
print(a,b)
# -

# ## GridFigure
#
# 元のmatplotlibはpyplot.axesメソッドで自由にsubplotを配置できる.
#
# subplot のグリッド配置を直感的に行えるようにする.
#
# * 各subplotのプロットエリアサイズを直接指定する.
#
# 既存のsubplotを基準として, 位置を相対的に指定できる.
#
# * gf.add_right(a) した後に, もう一度gf.add_right(a) した場合の挙動をどうするか.
#     1. [x] 既存のsubplot上に重なるようにする.
#         * 入れ子のサブプロットができるようにする
#     2. [ ] 既存のsubplotの右に追加する.
#         * subplot間の関係のマップを作る必要がある

# +
# Tests
padding={
    "left":0,
    "right":0,
    "top":0,
    "bottom":0
}


gf = MatPos()

"""
a a a a
a a a a
a a a a
"""
a = gf.from_left_top(gf,(4,3))
print(
    a.size == (4,3), 
    a.origin == (0,0),
    gf.left_top == (0,0),
    gf.right_bottom == (4,3)
)


"""
a a a a
a a a a b
a a a a b
"""
b = gf.add_right(a, (1,None), offset=(0,1))
print(
    b.size == (1,2), 
    b.origin == (4,1),
    gf.left_top == (0,0),
    gf.right_bottom == (5,3)
)

"""
  a a a a 
  a a a a b
  a a a a b
c c c c c c
"""

c = gf.add_bottom(a, (None,1),offset=(-1,0))
print(
    c.size == (6,1), 
    c.origin == (-1,3),
    gf.left_top == (-1,0),
    gf.right_bottom == (5,4)
)

"""
  d d a a 
  d d a a b
  a a a a b
c c c c c c
"""

d = gf.from_left_top(a, (2,2))
print(
    d.size == (2,2), 
    d.origin == (0,0),
    gf.left_top == (-1,0),
    gf.right_bottom == (5,4)
)

print(
    gf.get_size() == (6,4),
)


print(
    gf.relative(a, padding) == ((1/6, 0), (5/6, 3/4)),
    gf.relative(b, padding) == ((5/6, 1/4), (1, 3/4)),
    gf.relative(c, padding) == ((0, 3/4), (1,1)),
    gf.relative(d, padding) == ((1/6, 0), (3/6, 2/4))
)

print(
    gf.axes_position(a, padding),
    gf.axes_position(b, padding),
    gf.axes_position(c, padding),
    gf.axes_position(d, padding)
)

fig, axes = gf.figure_and_axes([a,b,c,d],padding=padding, facecolor="gray")

axes[0].text(0.5,0.5,"a")
axes[1].text(0.5,0.5,"b")
axes[2].text(0.5,0.5,"c")
axes[3].text(0.5,0.5,"d")



# +
# Tests

gf = MatPos()

a = gf.from_left_top(gf,(4,3))
b = gf.add_right(a, (1,None), offset=(0.5,1))
c = gf.add_bottom(a, (None,1),offset=(1,0.5))


fig, axes = gf.figure_and_axes([a,b,c], padding={"left":1,"right":1,"top":1,"bottom":1})

axes[0].text(0.5,0.5,"a")
axes[1].text(0.5,0.5,"b")
axes[2].text(0.5,0.5,"c")



# +
# Tests

gf = MatPos()

a = gf.from_left_top(gf,(4,3))
b = gf.add_right(a, (1,None), offset=(0.5,1))
c = gf.add_bottom(a, (None,1),offset=(1,0.5))
d = gf.from_left_top(a, (2,1.5), offset=(0,.5))

print(gf.get_size())
fig, axes = gf.figure_and_axes([a,b,c,d],figsize=(4,4))

axes[0].text(0.5,0.5,"a")
axes[1].text(0.5,0.5,"b")
axes[2].text(0.5,0.5,"c")
axes[3].text(0.5,0.5,"d")
axes[3].set_xticks([])
axes[3].set_yticks([])

# +
# Tests

gf = MatPos()

a = gf.add_bottom(gf,(6,3))
b = gf.add_bottom(a, (6,3), offset=(0,0.5))
c = gf.add_bottom(b, (6,3), offset=(0,0.5))
d = gf.add_bottom(c, (6,3), offset=(0,0.5))

fig,axes = gf.figure_and_axes([a,b,c,d])


axes[0].text(0.5,0.5,"a")
axes[1].text(0.5,0.5,"b")
axes[2].text(0.5,0.5,"c")
axes[3].text(0.5,0.5,"d")

# -

# Subplot のサイズ指定方法について
#
# * Default: 同じサイズのsubplotを行列に並べる. 列数を指定
# * Later: データとアクションを指定した後からサイズを指定
# * Contemporaly: データ指定時にサイズも指定
# * Prior: 先にサイズを指定しておいて後からデータを流し込む
#
# ```python
# figure = Figure()
#
# a = figure.add_bottom(subplot_a, size, offset)
# b = figure.add_bottom(subplot_b, size, offset, a)
#
# figure.align(gridder.figure_and_axes([a,b])
# figure.show(gridder.figure_and_axes([a,b]))
#              
# # grid layout
# figure = Figure.grid(column)
# a = figure.add_subplot(subplot_a, size, offset)
# b = figure.add_subplot(subplot_a, size, offset)
# ```

# +
gf = MatPos()



"""
reduce(
    acc, e -> acc,
    es,
    init
)
"""


sgs =  gf.add_grid([(4,1),(4,2.5),(4,1)], 2, (0.5,0.5))

d = gf.add_right(sgs[1], (4,None), (0.5,0))

fig, axes = gf.figure_and_axes([*sgs,d])

# +
gf = MatPos({"left":1, "right":1, "top":1,"bottom":1})

"""
1 2 3
4 5 6
7 8 9
"""

"""
reduce(
    acc, e -> acc,
    es,
    init
)
"""


sgs =  gf.add_grid([(2,2) for i in range(9)], 3, (1,0.5))
print(gf.get_size())
print(gf.left_top)
fig, axes = gf.figure_and_axes(sgs)

# +
mp = MatPos()

a = mp.add_bottom(mp,(2,2))
b = mp.add_top(a, (1,1), margin=0.5)
c = mp.add_right(a, (1,1), margin=0.5)
d = mp.add_bottom(a, (1,1), margin=0.5)
e = mp.add_left(a, (1,1), margin=0.5)

fig, axes = mp.figure_and_axes([a,b,c,d,e],padding={"left":1, "right":1, "top":1,"bottom":1})

axes[0].text(0.5,0.5,"a")
axes[1].text(0.5,0.5,"b")
axes[2].text(0.5,0.5,"c")
axes[3].text(0.5,0.5,"d")
axes[4].text(0.5,0.5,"e")
# -


