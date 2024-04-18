import numpy as np

# simulate drone positions
positions = np.random.rand(10, 2)
positions = np.zeros((10, 2))

print(positions)

# calculate pairwise distances between drones
distance_matrix = np.sqrt(np.sum((positions[:, np.newaxis] - positions) ** 2, axis=-1))
print(type(distance_matrix), distance_matrix.shape)
print(distance_matrix)

# set collision threshold
collision_threshold = 0.1

# check for collisions
for i in range(distance_matrix.shape[0]):
    for j in range(i+1, distance_matrix.shape[1]):
        if distance_matrix[i,j] < collision_threshold:
            print(f"Collision detected between drones {i} and {j}")
