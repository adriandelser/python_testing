from rtree import index
from shapely.geometry import box, Point

# left, bottom, right, top = (0.0, 0.0, 1.0, 1.0)

# idx = index.Index()

# idx.insert(0, (left,bottom,right,top))

# query_box = box(1.1, 1.1, 2.0, 2.0)
# # print(query_box.bounds)
# result = list(idx.intersection(query_box.bounds))

# print(result)


min_x, min_y, max_x, max_y = (-0.974927, -0.900968, 0.974927, 1.0)
drone_position = (-3, 0)

def create_rtree_index(rtree_index:index.Index):
    bbox = box(min_x, min_y, max_x, max_y)
    rtree_index.insert(0, bbox.bounds)
    print(f"{rtree_index=}")

def get_nearby_buildings(drone_position, threshold_distance:float, rtree_index):
    # print(f"{drone_position=}, {drone_position[0] - threshold_distance=}")
    query_box = box(-8.0, -4.9999, 2.0, 5.0001)
    print(f"{query_box.bounds=}")
    potential_buildings = list(rtree_index.intersection(query_box.bounds))
    print(f"{potential_buildings=}")
    # nearby_buildings = []
    # for i in potential_buildings:
    #     building_polygon = self.buildings[i].get_bounding_box()  # or however you represent the building shape
    #     drone_point = Point(drone_position)
    #     distance = drone_point.distance(building_polygon)
    #     if distance < threshold_distance:
    #         nearby_buildings.append(self.buildings[i])
    # return nearby_buildings


rtree_index = index.Index()
create_rtree_index(rtree_index)

nearby = get_nearby_buildings(drone_position, 5, rtree_index)

print(nearby)
