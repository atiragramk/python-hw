import numpy as np
from math import e

a = np.zeros((4, 3), dtype=np.int32)
b = np.ones((4, 3),  dtype=np.int32)
c = np.arange(12).reshape((4, 3))

x_1 = np.arange(0, 101)
x_2 = np.arange(-10, 11)

fx_1 = 2 * x_1 ** 2 + 5
fx_2 = np.power(e, -x_2)

np.column_stack((x_1, fx_1))
np.column_stack((x_2, fx_2))
