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

from src.matpos import MatPos
import matplotlib.pyplot as plt

# +
mp = MatPos()

a = mp.add_right(mp,(4,3))
b = mp.add_right(a,(4,3))
c = mp.add_bottom(a,(None,3))

_,axs = mp.figure_and_axes([a,b,c])

plt.savefig("./test.png")

# +
mp = MatPos()

sgs = mp.add_grid([(4,3) for i in range(6)], 2 , (0.5,0.5))
_,axs = mp.figure_and_axes(sgs)
plt.savefig("./test.png")
