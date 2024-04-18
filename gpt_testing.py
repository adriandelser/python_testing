import numpy as np
from scipy.spatial import distance
import warnings

def generate_coordinates(n_drones, side_length, min_distance):
    max_iterations = 10000  # Define a limit on the number of iterations
    iteration = 0
    starting_positions = []
    ending_positions = []

    density = n_drones * (np.pi * (min_distance/2)**2) / (side_length**2)
    if density > 0.8:
        warnings.warn(f"Drone density ({density}) or minimum distance might be too high for the side length. Adjust the parameters.")

    while len(starting_positions) < n_drones and iteration < max_iterations:
        new_start = np.random.uniform(0, side_length, 2)  # Generate a new start 2D point
        new_end = np.random.uniform(0, side_length, 2)  # Generate a new end 2D point

        if starting_positions:
            dists = distance.cdist([new_start], starting_positions, 'euclidean')[0]
            if np.min(dists) < min_distance:
                iteration += 1
                continue  # Skip this point, it's too close

        if ending_positions:
            dists = distance.cdist([new_end], ending_positions, 'euclidean')[0]
            if np.min(dists) < min_distance:
                iteration += 1
                continue  # Skip this point, it's too close

        # If the point passed all checks, add it to both starting and ending positions
        starting_positions.append(new_start)
        ending_positions.append(new_end)

    if iteration == max_iterations:
        warnings.warn(f"Maximum iteration reached. Returning available positions."
                      f"There are {len(starting_positions)} available drones")

    return starting_positions, ending_positions

a, b = generate_coordinates(n_drones=150,side_length=8,min_distance=0.5)

#print(a,b)