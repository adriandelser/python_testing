from shapely.ops import nearest_points
from shapely.geometry import Point, Polygon, LineString
import matplotlib.pyplot as plt
import time
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
        print(f"{next_panel=}, {panel}")
        panels2D.append((next_panel.x,next_panel.y))
        time.sleep(1)
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
    plt.plot(*opposite_point.xy, 'ro')

    #set the aspect ratio to 1 (by getting current axes)
    ax = plt.gca()

    ax.set_aspect('equal', adjustable='box')

    plt.show()

    plt.plot(panels1D)
    plt.show()