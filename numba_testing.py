import numpy as np
from numba import jit
import time

@jit(nopython=True)
def euclidean_distance_numba(point1, point2):
    '''Why is this docstring not highlighted'''
    return np.sqrt(np.sum((point1 - point2) ** 2))

point1 = np.array([1.0, 2.0, 3.0])
point2 = np.array([4.0, 5.0, 6.0])

# Time the first call (includes compilation time)
start_time = time.time()
print(euclidean_distance_numba(point1, point2))
print("First call time:", time.time() - start_time)

# Time the second call (uses compiled code)
start_time = time.time()
print(euclidean_distance_numba(point1, point2))
print("Second call time:", time.time() - start_time)
