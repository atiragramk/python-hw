import numpy as np
from math import e

a = np.zeros((4, 3), dtype=np.integer)
b = np.ones((4, 3),  dtype=np.integer)
c = np.arange(11)

x_1 = np.arange(0, 101)
x_2 = np.arange(-10, 11)

fx_1 = x_1 * 2 ** 2 + 5
fx_2 = np.power(e, -x_2)
