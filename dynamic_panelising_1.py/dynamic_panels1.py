import numpy as np
import time

class CascadingArrays:
    def __init__(self, arrays, max_values):
        self.arrays = arrays
        self.max_values = max_values

    def add(self, value):
        # Increment all arrays first
        for i in range(len(self.arrays)):
            self.arrays[i] += value

        # Then cascade
        for i in range(len(self.arrays)):
            self.cascade(i)

    def cascade(self, index):
        current_index = index
        next_index = (current_index + 1) % len(self.arrays)
        overflow = self.arrays[current_index] > self.max_values[current_index]

        while np.any(overflow):
            # Process overflow
            overflow_values = self.arrays[current_index][overflow] - self.max_values[current_index]
            self.arrays[current_index] = self.arrays[current_index][~overflow]

            # Cascade overflow values to next array
            while np.any(overflow_values > self.max_values[next_index]):
                new_overflow = overflow_values > self.max_values[next_index]
                non_overflow_values = overflow_values[~new_overflow]
                self.arrays[next_index] = np.insert(self.arrays[next_index], 0, non_overflow_values)
                overflow_values = overflow_values[new_overflow] - self.max_values[next_index]
                current_index = next_index
                next_index = (current_index + 1) % len(self.arrays)

            self.arrays[next_index] = np.insert(self.arrays[next_index], 0, overflow_values)

            # Update overflow for the next iteration
            overflow = self.arrays[current_index] > self.max_values[current_index]

# Example usage
arrays = [np.array([1.0, 2.0]), np.array([1.0, 2.0]), np.array([3.0, 4.0])]
max_values = [5, 5, 5]
cascading_arrays = CascadingArrays(arrays, max_values)

# Add a value
t= time.perf_counter()
cascading_arrays.add(10)
t = time.perf_counter()-t
print(t)
# Check the arrays after addition
print([arr.tolist() for arr in cascading_arrays.arrays])
