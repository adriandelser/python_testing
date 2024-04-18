import numpy as np
import time
def distance_to_point(polygon, point):
    def on_segment(p, q, r):
        """Check if point q lies on line segment 'pr'"""
        if (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1])):
            return True
        return False

    def distance(p1, p2):
        """Euclidean distance between two points"""
        return np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

    total_distance = 0.0

    for i in range(len(polygon)):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % len(polygon)]

        if on_segment(p1, point, p2):
            total_distance += distance(p1, point)
            return total_distance
        else:
            total_distance += distance(p1, p2)

    return -1  # Point is not on the perimeter

# Example usage
polygon = np.array([[0, 0], [2, 0], [2, 2], [0, 2]])
point = np.array([2, 3])
t= time.perf_counter()
distance_to_point(polygon, point)
t= time.perf_counter()-t
print(f"{t=}")
print(distance_to_point(polygon, point))
