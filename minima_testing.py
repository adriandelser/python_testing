from scipy.signal import argrelextrema
import numpy as np
import matplotlib.pyplot as plt

from time import time
# Define a larger scalar field with multiple local minima
# field = np.array([[6, 9, 6, 8, 6],
#                   [9, 2, 5, 1, 7],
#                   [6, 5, 4, 7, 8],
#                   [7, 2, 7, 2, 9],
#                   [8, 7, 6, 8, 7]])

# Function to compare a point with its neighbors in a specific axis
def compare_with_neighbors(array, axis):
    def compare(x, y):
        return np.less(x, y)
    return argrelextrema(array, compare, axis=axis)

# # Find the local minima along each axis
# minima_x = compare_with_neighbors(field, 0)
# minima_y = compare_with_neighbors(field, 1)

# # Convert the results to sets of tuples
# minima_x = set(zip(minima_x[0], minima_x[1]))
# minima_y = set(zip(minima_y[0], minima_y[1]))

# # Find the intersection of the two sets
# true_minima_locations = list(minima_x & minima_y)

# true_minima_locations





import numpy as np

def generate_random_field(size, seed=None):
    """
    Generate a random 2D scalar field with the given size.
    
    The values in the field are generated from a uniform distribution over [0, 1).
    
    Parameters
    ----------
    size : int
        The size of the field. The field will have size x size cells.
    seed : int, optional
        The seed for the random number generator.
    
    Returns
    -------
    field : numpy.ndarray
        The generated field.
    """
    if seed is not None:
        np.random.seed(seed)
        
    field = np.random.rand(size, size)
    
    return field

# Generate a random field with size 10x10
field = generate_random_field(31, seed=42)


t = time()
# Find the local minima along each axis
minima_x = compare_with_neighbors(field, 0)
minima_y = compare_with_neighbors(field, 1)

# Convert the results to sets of tuples
minima_x = set(zip(minima_x[0], minima_x[1]))
minima_y = set(zip(minima_y[0], minima_y[1]))

# Find the intersection of the two sets
true_minima_locations = list(minima_x & minima_y)

# Identify the values of the local minima
minima_values = field[tuple(np.array(true_minima_locations).T)]

# Find the index of the lowest local minimum
lowest_minima_index = np.argmin(minima_values)

# Find the coordinates and value of the lowest local minimum
lowest_minima_location = true_minima_locations[lowest_minima_index]
lowest_minima_value = minima_values[lowest_minima_index]

print(f'{lowest_minima_location = }, {lowest_minima_value = }')

print(f'{time()-t = }, {1/(time()-t) = }')


# Show the field and the true local minima
# print(f'{field = }, {true_minima_locations = }')








# Create a scalar plot of the field
plt.figure(figsize=(10, 10))
plt.imshow(field, origin='lower', cmap='viridis')
plt.colorbar(label='Value')
plt.clim(np.min(field), np.max(field))

# Mark the true local minima
minima_y, minima_x = zip(*true_minima_locations)
plt.plot(minima_x, minima_y, 'r.', markersize=10)

# Mark the lowest local minimum
plt.plot(lowest_minima_location[1], lowest_minima_location[0], 'b.', markersize=15)


# Show the plot with labels
plt.title('Random Scalar field with true local minima marked')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
plt.show()


def find_global_minimum(array):
    '''given a 2d scalar array, find the location of the global minimum please please'''
    def compare(x, y):
        return np.less(x, y)
    return argrelextrema(array, compare, axis=None)

print(find_global_minimum(field))

    