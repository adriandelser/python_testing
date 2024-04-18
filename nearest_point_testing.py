#%%
from shapely.ops import nearest_points
from shapely.geometry import Point, Polygon, LineString
import matplotlib.pyplot as plt
import time
import sys



def find_vertex_after_point(polygon:Polygon, point:tuple)->int|None:
    """Returns the edge that contains the given point, along with its index in the perimeter.
    If the point is one of the vertices of the polygon, it will return the point and its index.
    If the point is not on the perimeter, it will return None.
    If the point is on the perimeter, it will return the edge that contains the point and its index.
    The index will be the index of the first vertex of the edge, not the point.
    If the point is on the edge, it will return the edge and its index.
    Args:
        polygon (Polygon): _description_
        point (tuple): _description_

    Returns:
        tuple: _description_
    """
    perimeter = polygon.exterior
    num_vertices = len(perimeter.coords)
    #if the point is one of the vertices, return it
    if point in perimeter.coords:
        point_idx = list(perimeter.coords).index(point)%(num_vertices-1)
        return point_idx

    point = Point(point)

    for i in range(num_vertices - 1):
        edge = LineString([perimeter.coords[i], perimeter.coords[i + 1]])
        if edge.contains(point):
            #return the index of the latter vertex of the edge
            return i+1

    return None


def move_point_along_perimeter(polygon:Polygon, point:tuple, length:float|int):
    perimeter_length = polygon.length
    #if the length is longer than the perimeter, make it the remainder 
    length = length % perimeter_length 
    perimeter = polygon.exterior

    coords = list(perimeter.coords)
    current_distance = 0
    current_point = Point(point)

    # Find the index of the vertex after the current point
    vertex_idx = find_vertex_after_point(polygon, point)
    # Rearrange coordinates so the loop starts from the vertex after the current point
    coords = coords[vertex_idx:] + coords[:vertex_idx]

    for i, p in enumerate(coords):
        next_point = Point(p)
        segment_length = current_point.distance(next_point)
        if current_distance + segment_length >= length:
            # Interpolate point on the segment
            remaining_length = length - current_distance
            ratio = remaining_length / segment_length
            new_x = current_point.x + ratio * (next_point.x - current_point.x)
            new_y = current_point.y + ratio * (next_point.y - current_point.y)
            return Point(new_x, new_y)

        current_distance += segment_length
        current_point = next_point

    #return initial point if there are any issues 
    # NOTE this might be unreachable if the function was properly designed
    return Point(point)

def generate_half_line_positions(L, progression_func, smallest_gap, uniform_range,init_point:tuple, polygon:Polygon):
    midpoint = L / 2
    panels = [Point(init_point)]
    positions = [0]

    print(f"{polygon=}")
    # Generate panels for one side (e.g., right side) of the midpoint
    gap = smallest_gap
    while positions[-1] < L:
        # Check if the next position is within the uniform range
        if positions[-1] + gap - midpoint < uniform_range/2:
            gap = smallest_gap  # Keep the gap uniform
        else:
            gap = progression_func(gap)  # Increase the gap

        next_position = positions[-1] + gap
        next_panel = move_point_along_perimeter(polygon,panels[-1],gap)
        if next_position < L:
            positions.append(next_position)
            panels.append(next_panel)
        else:
            break

    # return [p-midpoint for p in positions]
    return panels


if __name__ == "__main__":
    h = 6
    polygon = Polygon([(0, 0), (6, 0), (6, h),(3,h+4), (0, h), (-4, h/2)])
    perimeter = polygon.length
    print(f"{perimeter=}")
    point = Point(7, 2)
    p1, p2 = nearest_points(polygon, point)
    input_point = (p1.x, p1.y)
    new_point = move_point_along_perimeter(polygon, input_point, 3*perimeter/2)
    print(f"{move_point_along_perimeter(polygon, (6,6), 1)=}")

    t = time.perf_counter()
    # panels1D = generate_half_line_positions(L=perimeter,progression_func=lambda gap:1.1*gap, smallest_gap=0.2,uniform_range=1)
    # print(f"{panels1D=}")
    print(f"{time.perf_counter() - t=}")
    progression_func = lambda gap: gap * 2
    panels2D = generate_half_line_positions(perimeter, progression_func, smallest_gap=0.5, uniform_range= 0.5, init_point=input_point,polygon= polygon)
    # print(panels2D)
    # for panel in panels1D:
    #     next_panel = move_point_along_perimeter(polygon,input_point,panel)
    #     panels2D.append((next_panel.x,next_panel.y))
    print(f"{time.perf_counter() - t=}")

    # sys.exit()
    # panel_positions = generate_panel_positions_on_polygon(polygon, Point(input_point), progression_func, 0.2, 1)

    # print(f"{panel_positions=}")


    # print(f"{time.perf_counter() - t=}")
    x_coords = [point.x for point in panels2D]
    y_coords = [point.y for point in panels2D]
    plt.scatter(x_coords, y_coords, marker='o')  # Plot points


    plt.plot(*polygon.exterior.xy)
    plt.plot(*point.xy, 'bo')
    plt.plot(*input_point, 'go')
    print(f"{input_point=}")
    plt.plot(*new_point.xy, 'ro')

    #set the aspect ratio to 1 (by getting current axes)
    ax = plt.gca()

    ax.set_aspect('equal', adjustable='box')

    plt.show()

#%%
def generate_panels_along_perimeter(perimeter_length, max_distance, base_spacing):
    positions = []
    current_position = 0
    increasing_factor = max_distance / perimeter_length

    while current_position < max_distance:
        positions.append(current_position)
        # Increase the spacing for each subsequent panel
        spacing = base_spacing + (current_position * increasing_factor)
        current_position += spacing

    return positions

# Example usage
perimeter_length = 10  # Total perimeter length
max_distance = 5      # Maximum distance along the perimeter
base_spacing = 0.5    # Initial spacing between panels

panel_positions = generate_panels_along_perimeter(perimeter_length, max_distance, base_spacing)
print(panel_positions)

# %%
import numpy as np
from scipy.stats import norm

def generate_panels_normal_distribution(max_distance, std_dev, base_spacing):
    # Generate a range of values from 0 to max_distance
    values = np.linspace(0, max_distance, 1000)
    
    # Get the CDF values for these points
    cdf_values = norm.cdf(values, loc=0, scale=std_dev)

    # Determine panel positions based on the CDF
    positions = [base_spacing]
    while positions[-1] < max_distance:
        next_position = np.interp(positions[-1] + base_spacing, cdf_values, values)
        if next_position < max_distance:
            positions.append(next_position)
        else:
            break

    return positions

# Example usage
max_distance = 5   # Maximum distance along the perimeter
std_dev = 1        # Standard deviation for the normal distribution
base_spacing = 0.5 # Initial spacing between panels

panel_positions = generate_panels_normal_distribution(max_distance, std_dev, base_spacing)
print(panel_positions)

# %%
def generate_panels_inverse_distance(max_distance, base_spacing):
    positions = [0]
    while positions[-1] < max_distance:
        # Calculate the next position
        inverse_distance = 1 / (positions[-1] + 1)  # Adding 1 to avoid division by zero
        next_position = positions[-1] + base_spacing * inverse_distance
        if next_position < max_distance:
            positions.append(next_position)
        else:
            break

    return positions

# Example usage
max_distance = 5   # Maximum distance along the perimeter
base_spacing = 0.5 # Initial spacing between panels

panel_positions = generate_panels_inverse_distance(max_distance, base_spacing)
print(panel_positions)










# %%
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

def divide_line_into_panels(line_length, distribution, num_samples=100):
    # Generate sample points along the line
    sample_points = np.linspace(0, line_length, num_samples)
    
    # Evaluate the distribution at these points
    density_values = distribution.pdf(sample_points)
    density_values = 1/density_values
    # Normalize the density values so their sum equals the line length
    density_values *= line_length / density_values.sum()

    # Determine panel boundaries
    panel_boundaries = [0]
    for density in density_values:
        next_boundary = panel_boundaries[-1] + density
        if next_boundary <= line_length:
            panel_boundaries.append(next_boundary)

    # Convert boundaries to panel lengths
    panels = np.diff(panel_boundaries)

    return panels, sample_points, 1/density_values

# Example usage
L = 10  # Length of the line
mean = L / 2  # Center of the normal distribution
std_dev = 2   # Standard deviation
samples = 20
# Normal distribution centered in the middle of the line
normal_dist = norm(loc=mean, scale=std_dev)

panels, sample_points, density_values = divide_line_into_panels(L, normal_dist, num_samples=samples)
print(f"{len(panels)=}")

# Visualization
plt.figure(figsize=(12, 6))

# Plot the distribution
plt.plot(sample_points, density_values, label='Distribution', color='blue')

# Mark the panels
for panel_boundary in np.cumsum(panels):
    plt.axvline(panel_boundary, color='red', linestyle='--')

plt.title('Panel Distribution Along the Line')
plt.xlabel('Position along the line')
plt.ylabel('Density')
plt.legend()
plt.show()

# %%
def symmetric_inverse_distance_distribution(line_length, num_samples=1000, offset=0.1):
    # Calculate the midpoint of the line
    midpoint = line_length / 2

    # Generate sample points along the line
    sample_points = np.linspace(0, line_length, num_samples)

    # Calculate the symmetric distance from the midpoint
    symmetric_dist = np.abs(sample_points - midpoint)

    # Calculate the 1/(distance + offset) values
    inv_dist_values = 1 / (symmetric_dist + offset)

    return inv_dist_values

def normal_distribution_function(line_length, num_samples, std_dev=1):
    # Calculate the midpoint of the line
    midpoint = line_length / 2

    # Generate sample points along the line
    sample_points = np.linspace(0, line_length, num_samples)

    # Calculate the normal distribution values
    normal_dist_values = norm.pdf(sample_points, loc=midpoint, scale=std_dev)

    return normal_dist_values

from scipy.optimize import minimize_scalar

def find_std_dev_for_smallest_gap(L, smallest_gap):
    midpoint = L / 2
    target_cdf_diff = smallest_gap / L

    def objective(std_dev):
        point1 = midpoint - smallest_gap / 2
        point2 = midpoint + smallest_gap / 2
        cdf_diff = norm.cdf(point2, loc=midpoint, scale=std_dev) - norm.cdf(point1, loc=midpoint, scale=std_dev)
        return (cdf_diff - target_cdf_diff) ** 2

    # Use minimize_scalar to find the optimal standard deviation
    result = minimize_scalar(objective, bounds=(0, L), method='bounded')

    if result.success:
        return result.x
    else:
        raise ValueError("Optimization did not converge")




def divide_line_into_panels_custom_dist(line_length, num_samples, custom_distribution, **kwargs):
    # Get the custom distribution values
    density_values = custom_distribution(line_length, num_samples, **kwargs)

    # Invert and normalize the density values
    inverted_density_values = 1 / density_values
    inverted_density_values *= line_length / inverted_density_values.sum()

    # Determine panel boundaries
    panel_boundaries = [0]
    for density in inverted_density_values:
        next_boundary = panel_boundaries[-1] + density
        if next_boundary <= line_length:
            panel_boundaries.append(next_boundary)

    # Convert boundaries to panel lengths
    panels = np.diff(panel_boundaries)
    # print(f"{panels=}")
    # print(f"{panel_boundaries=}")

    return panels, density_values, inverted_density_values


# Example usage
L = 10  # Length of the line
mean = L / 2  # Center of the normal distribution
smallest_gap = L / 100
std_dev = find_std_dev_for_smallest_gap(L, smallest_gap)
print(f"{std_dev=}")
# std_dev = L/4   # Standard deviation
samples = 100
# Using the normal distribution for panel division
t= time.perf_counter()
panels, density_values, inverted_density_values = divide_line_into_panels_custom_dist(
    line_length=L,num_samples=samples,custom_distribution= normal_distribution_function, std_dev= std_dev)
print(f"{time.perf_counter()-t=}")

# Visualization
plt.figure(figsize=(12, 6))

# Plot the original normal distribution
plt.plot(np.linspace(0, L, samples), density_values, label='Normal Distribution', color='blue')

# Plot the inverted distribution (for panel sizing)
# plt.plot(np.linspace(0, L, 1000), inverted_density_values, label='Inverted Normal Distribution (for Panel Sizing)', color='green')
# print(f"{np.cumsum(panels)=}")
# Mark the panels
for panel_boundary in np.cumsum(panels):
    plt.axvline(panel_boundary, color='red', linestyle='--')

plt.title('Panel Distribution Along the Line with Normal Distribution')
plt.xlabel('Position along the line')
plt.ylabel('Density')
plt.legend()
plt.show()

# %%
from scipy.stats import norm
from scipy.optimize import minimize_scalar
import time
from scipy.integrate import quad

def estimate_num_samples(L, smallest_gap):
    midpoint = L / 2
    target_cdf_diff = smallest_gap / L

    def objective(std_dev):
        point1 = midpoint - smallest_gap / 2
        point2 = midpoint + smallest_gap / 2
        cdf_diff = norm.cdf(point2, loc=midpoint, scale=std_dev) - norm.cdf(point1, loc=midpoint, scale=std_dev)
        return (cdf_diff - target_cdf_diff) ** 2

    # Find the standard deviation
    result = minimize_scalar(objective, bounds=(0, L), method='bounded')
    if not result.success:
        raise ValueError("Optimization did not converge")

    std_dev = result.x

    # Estimate the number of samples
    # Integrate the normal distribution across the line
    total_area, _ = quad(lambda x: norm.pdf(x, loc=midpoint, scale=std_dev), 0, L)
    # Area corresponding to the smallest gap
    gap_area = norm.pdf(midpoint, loc=midpoint, scale=std_dev) * smallest_gap

    # Estimate the number of samples
    num_samples = total_area / gap_area

    return std_dev, int(num_samples)

# Example usage
L = 10
smallest_gap = 1 / 100
try:
    t=time.perf_counter()
    std_dev, estimated_samples = estimate_num_samples(L, smallest_gap)
    print(time.perf_counter()-t)
    print("Calculated Standard Deviation:", std_dev)
    print("Estimated Number of Samples:", estimated_samples)
except ValueError as e:
    print(e)





# %%
# import numpy as np
import time
# import numba

def generate_panel_positions(L, progression_func, smallest_gap,uniform_range):
    midpoint = L / 2
    positions = [midpoint]

    # Start adding panels, alternating on each side of the midpoint
    gap = smallest_gap
    while positions[0] > 0 and positions[-1] < L:
        next_left = positions[0] - gap
        next_right = positions[-1] + gap

        gap = progression_func(gap)
        # Check if the next positions are within the uniform range
        if abs(midpoint - next_left) < uniform_range/2 or abs(midpoint - next_right) < uniform_range/2:
            gap = smallest_gap  # Keep the gap uniform
        else:
            gap = progression_func(gap)  # Increase the gap

        if positions[0]>0:
            positions.insert(0, next_left)
        if positions[-1] < L:
            positions.append(next_right)
        

        # time.sleep(1)



    return positions[1:-1]

# Example usage
L = 10
uniform_range = 1
smallest_gap = 0.01

# Define a simple progression function, e.g., increase gap by 10% each time
progression_func = lambda gap: gap * 1.05
t = time.perf_counter()
panel_positions = generate_panel_positions(L, progression_func, smallest_gap,uniform_range)
print(f"{time.perf_counter()-t}")
print(f"{len(panel_positions)=}")
for panel in panel_positions:
    plt.axvline(panel, ymin=0, ymax=1)
# print(panel_positions)

plt.show()

# %%
import time
def generate_half_line_positions(L, progression_func, smallest_gap, uniform_range):
    midpoint = L / 2
    positions = [midpoint]

    # Generate panels for one side (e.g., right side) of the midpoint
    gap = smallest_gap
    while positions[-1] < L:
        # Check if the next position is within the uniform range
        if positions[-1] + gap - midpoint < uniform_range/2:
            gap = smallest_gap  # Keep the gap uniform
        else:
            gap = progression_func(gap)  # Increase the gap

        next_position = positions[-1] + gap
        if next_position < L:
            positions.append(next_position)
        else:
            break

    return positions

def mirror_positions(positions, L):
    # Mirror the positions across the midpoint
    mirrored = [L - pos for pos in positions[::-1]]
    return mirrored[:-1] + positions  # Exclude the midpoint from one side to avoid duplication

# Example usage
L = 10
uniform_range = 1  # 10% of L around the midpoint
smallest_gap = 0.01

# Define a simple progression function, e.g., increase gap by 10% each time
progression_func = lambda gap: gap * 1.1
t= time.perf_counter()
half_line_positions = generate_half_line_positions(L, progression_func, smallest_gap, uniform_range)
panel_positions = mirror_positions(half_line_positions, L)
print(time.perf_counter()-t)
# print(panel_positions)
for panel in panel_positions:
    plt.axvline(panel, ymin=0, ymax=1)
# print(panel_positions)

plt.show()

# %%
import numpy as np
from shapely.geometry import Polygon
from shapely.ops import nearest_points

def calculate_perimeter(polygon):
    return polygon.length

def find_point_on_perimeter(polygon, distance):
    perimeter = polygon.exterior
    current_distance = 0
    for i in range(len(perimeter.coords) - 1):
        p1 = np.array(perimeter.coords[i])
        p2 = np.array(perimeter.coords[i + 1])
        segment_length = np.linalg.norm(p2 - p1)

        if current_distance + segment_length >= distance:
            remainder = distance - current_distance
            point = p1 + (p2 - p1) * (remainder / segment_length)
            return point

        current_distance += segment_length

def generate_panel_positions_on_polygon(polygon, highest_density_point, progression_func, smallest_gap, uniform_range):
    L = calculate_perimeter(polygon)
    # Convert highest density point to distance along the perimeter
    distance_at_highest_density = polygon.project(highest_density_point)

    # Generate panel positions (distances) along the perimeter
    half_line_positions = generate_half_line_positions(L, progression_func, smallest_gap, uniform_range)
    # Offset positions by the distance at the highest density point
    panel_distances = [(pos + distance_at_highest_density) % L for pos in half_line_positions]

    # Find the corresponding points on the polygon perimeter
    panel_positions = [find_point_on_perimeter(polygon, dist) for dist in panel_distances]

    return panel_positions

# Example usage
# Define your polygon and highest density point here
polygon = Polygon([(0, 0), (4, 0), (4, 3), (0, 3)])
highest_density_point = nearest_points(polygon, Point(2, 1.5))[0]  # Example point on the polygon

# Define the progression function, smallest gap, and uniform range
progression_func = lambda gap: gap * 1.1
smallest_gap = 1
uniform_range = calculate_perimeter(polygon) / 10

panel_positions = generate_panel_positions_on_polygon(polygon, highest_density_point, progression_func, smallest_gap, uniform_range)


# %%
def find_vertex_after_point(polygon:Polygon, point:tuple)->int|None:
    """Returns the edge that contains the given point, along with its index in the perimeter.
    If the point is one of the vertices of the polygon, it will return the point and its index.
    If the point is not on the perimeter, it will return None.
    If the point is on the perimeter, it will return the edge that contains the point and its index.
    The index will be the index of the first vertex of the edge, not the point.
    If the point is on the edge, it will return the edge and its index.
    Args:
        polygon (Polygon): _description_
        point (tuple): _description_

    Returns:
        tuple: _description_
    """
    perimeter = polygon.exterior
    num_vertices = len(perimeter.coords)
    #if the point is one of the vertices, return it
    if point in perimeter.coords:
        point_idx = list(perimeter.coords).index(point)%(num_vertices-1)
        return point_idx

    point = Point(point)

    for i in range(num_vertices - 1):
        edge = LineString([perimeter.coords[i], perimeter.coords[i + 1]])
        if edge.contains(point):
            #return the index of the latter vertex of the edge
            return i+1

    return None


def move_point_along_perimeter(polygon:Polygon, point:tuple, length:float|int):
    perimeter_length = polygon.length
    #if the length is longer than the perimeter, make it the remainder 
    length = length % perimeter_length 
    perimeter = polygon.exterior

    coords = list(perimeter.coords)
    current_distance = 0
    current_point = Point(point)

    # Find the index of the vertex after the current point
    vertex_idx = find_vertex_after_point(polygon, point)
    # Rearrange coordinates so the loop starts from the vertex after the current point
    coords = coords[vertex_idx:] + coords[:vertex_idx]

    for i, p in enumerate(coords):
        next_point = Point(p)
        segment_length = current_point.distance(next_point)
        if current_distance + segment_length >= length:
            # Interpolate point on the segment
            remaining_length = length - current_distance
            ratio = remaining_length / segment_length
            new_x = current_point.x + ratio * (next_point.x - current_point.x)
            new_y = current_point.y + ratio * (next_point.y - current_point.y)
            return Point(new_x, new_y)

        current_distance += segment_length
        current_point = next_point

    #return initial point if there are any issues 
    # NOTE this might be unreachable if the function was properly designed
    return Point(point)

def generate_half_line_positions(L, progression_func, smallest_gap, uniform_range):
    midpoint = L / 2
    # panels = [Point(init_point)]
    positions = [midpoint]

    # print(f"{polygon=}")
    # Generate panels for one side (e.g., right side) of the midpoint
    gap = smallest_gap
    while positions[-1] < L:
        # Check if the next position is within the uniform range
        if positions[-1] + gap < uniform_range/2:
            gap = smallest_gap  # Keep the gap uniform
        else:
            gap = progression_func(gap)  # Increase the gap
        print(f"{gap=}, {positions=}")
        # time.sleep(1)

        next_position = positions[-1] + gap
        # next_panel = move_point_along_perimeter(polygon,panels[-1],gap)
        if next_position < L:
            positions.append(next_position)
            # panels.append(next_panel)
        else:
            break

    # return [p-midpoint for p in positions]
    return positions
    # return panels

def mirror_positions(positions, L):
    # Mirror the positions across the midpoint
    print(f"{L=}")
    mirrored = [L - pos for pos in positions[::-1]]
    return mirrored[:-1] + positions  # Exclude the midpoint from one side to avoid duplication



if __name__ == "__main__":
    h = 6
    polygon = Polygon([(0, 0), (6, 0), (6, h),(3,h+4), (0, h), (-4, h/2)])
    perimeter = polygon.length
    print(f"{perimeter=}")
    point = Point(7, 2)
    p1, p2 = nearest_points(polygon, point)
    input_point = (p1.x, p1.y)
    opposite_point = move_point_along_perimeter(polygon, input_point, perimeter/2)
    print(f"{move_point_along_perimeter(polygon, (6,6), 1)=}")

    t = time.perf_counter()
    panels1D = generate_half_line_positions(L=perimeter,progression_func=lambda gap:1.5*gap, smallest_gap=1,uniform_range=1)
    panels1D = mirror_positions(panels1D, L=perimeter)
    print(f"{panels1D=}")

    # print(f"{panels1D=}")
    print(f"{time.perf_counter() - t=}")
    progression_func = lambda gap: gap * 2
    # panels2D = generate_half_line_positions(perimeter, progression_func, smallest_gap=0.5, uniform_range= 0.5, init_point=input_point,polygon= polygon)
    # print(panels2D)
    panels2D = [(opposite_point.x, opposite_point.y)]
    for panel in panels1D:
        next_panel = move_point_along_perimeter(polygon,(opposite_point.x, opposite_point.y),panel)
        panels2D.append((next_panel.x,next_panel.y))
    print(f"{time.perf_counter() - t=}")

    # sys.exit()
    # panel_positions = generate_panel_positions_on_polygon(polygon, Point(input_point), progression_func, 0.2, 1)

    # print(f"{panel_positions=}")


    # print(f"{time.perf_counter() - t=}")
    x_coords = [point[0] for point in panels2D]
    y_coords = [point[1] for point in panels2D]
    plt.scatter(x_coords, y_coords, marker='o')  # Plot points


    plt.plot(*polygon.exterior.xy)
    plt.plot(*point.xy, 'bo')
    plt.plot(*input_point, 'go')
    print(f"{input_point=}")
    plt.plot(*new_point.xy, 'ro')

    #set the aspect ratio to 1 (by getting current axes)
    ax = plt.gca()

    ax.set_aspect('equal', adjustable='box')

    plt.show()

    plt.plot(panels1D)
    plt.show()



# %%
