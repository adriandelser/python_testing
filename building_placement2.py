#%%
import random
# from rtree import index
import json
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon




# class QuadtreeNode:
#     def __init__(self, x, y, width, height):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.children = []
#         self.buildings = []

#     def subdivide(self):
#         half_width = self.width / 2
#         half_height = self.height / 2
#         self.children = [
#             QuadtreeNode(self.x, self.y, half_width, half_height),
#             QuadtreeNode(self.x + half_width, self.y, half_width, half_height),
#             QuadtreeNode(self.x, self.y + half_height, half_width, half_height),
#             QuadtreeNode(self.x + half_width, self.y + half_height, half_width, half_height)
#         ]

#     def insert_building(self, building):
#         x, y, size = building
#         # Check if the building can be placed in this node
#         if self.can_place_building(building):
#             self.buildings.append(building)
#             return True
#         else:
#             # Check if the building is too big for a potential child node or if max depth is reached
#             if size >= self.width / 2:# or self.depth >= self.max_depth:
#                 return False
#             if not self.children:
#                 self.subdivide()
#             # Attempt to place the building in one of the child nodes
#             for child in self.children:
#                 child.buildings = self.buildings
#                 if child.insert_building(building):
#                     return True
#             return False


#     def can_place_building(self, building):
#         x, y, size = building

#         # Check if the building is within the bounds of the node
#         if x + size > self.x + self.width or y + size > self.y + self.height or x < self.x or y < self.y:
#             return False

#         # Check for overlap with existing buildings
#         for existing_building in self.buildings:
#             ex, ey, esize = existing_building
#             # Check if buildings overlap
#             if not (x + size <= ex or ex + esize <= x or y + size <= ey or ey + esize <= y):
#                 return False

#         return True

class QuadtreeNode:
    def __init__(self, x, y, width, height, parent=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.parent = parent
        self.children = []
        self.buildings = []

    def subdivide(self):
        half_width = self.width / 2
        half_height = self.height / 2
        self.children = [
            QuadtreeNode(self.x, self.y, half_width, half_height, self),
            QuadtreeNode(self.x + half_width, self.y, half_width, half_height, self),
            QuadtreeNode(self.x, self.y + half_height, half_width, half_height, self),
            QuadtreeNode(self.x + half_width, self.y + half_height, half_width, half_height, self)
        ]

    def insert_building(self, building):
        if self.can_place_building(building):
            self.buildings.append(building)
            return True
        else:
            if not self.children and (self.width > 1 or self.height > 1):
                self.subdivide()

            for child in self.children:
                if child.insert_building(building):
                    return True
            return False

    def can_place_building(self, building):
        x, y, size = building

        # Check if the building is within the bounds of the node
        if x + size > self.x + self.width or y + size > self.y + self.height or x < self.x or y < self.y:
            return False

        # Check for overlap with existing buildings in this node
        for existing_building in self.buildings:
            ex, ey, esize = existing_building
            if not (x + size <= ex or ex + esize <= x or y + size <= ey or ey + esize <= y):
                return False

        # Check for overlap with buildings in parent nodes
        current_node = self.parent
        while current_node:
            for parent_building in current_node.buildings:
                px, py, psize = parent_building
                if not (x + size <= px or px + psize <= x or y + size <= py or py + psize <= y):
                    return False
            current_node = current_node.parent

        return True



class ScenarioGeneratorWithQuadtree:
    def __init__(self, area_bounds):
        self.quadtree_root = QuadtreeNode(area_bounds[0], area_bounds[1], area_bounds[2] - area_bounds[0], area_bounds[3] - area_bounds[1])
        self.scenario = {"alpha": {"buildings": [], "vehicles": []}}

    def add_random_buildings(self, n, building_size_range, max_attempts=1000):
        attempts = 0
        while len(self.scenario['alpha']['buildings']) < n and attempts < max_attempts:
            size = random.uniform(*building_size_range)
            x = random.uniform(self.quadtree_root.x, self.quadtree_root.x + self.quadtree_root.width - size)
            y = random.uniform(self.quadtree_root.y, self.quadtree_root.y + self.quadtree_root.height - size)
            building = (x, y, size)

            if not self.quadtree_root.insert_building(building):
                attempts += 1
            else:
                self.add_building(building)

    def add_building(self, building):
        x, y, size = building
        building_id = len(self.scenario['alpha']['buildings'])
        vertices = [[x, y], [x + size, y], [x + size, y + size], [x, y + size]]
        self.scenario['alpha']['buildings'].append({"ID": f"Building {building_id}", "vertices": vertices})

    # ... Other methods ...

    # Visualization method remains the same as your original code

    # def check_overlap(self, x, y, size):
    #     return list(self.building_index.intersection((x, y, x + size, y + size)))
    

    def add_vehicle(self, position, goal, source_strength, imag_source_strength, sink_strength, safety):
        vehicle_id = f"V{len(self.scenario['alpha']['vehicles']) + 1}"
        vehicle = {
            "ID": vehicle_id,
            "position": position,
            "goal": goal,
            "source_strength": source_strength,
            "imag_source_strength": imag_source_strength,
            "sink_strength": sink_strength,
            "safety": safety
        }
        self.scenario['alpha']['vehicles'].append(vehicle)

    def calculate_bounding_box(self, vertices):
        x_coords = [v[0] for v in vertices]
        y_coords = [v[1] for v in vertices]
        z_coords = [v[2] for v in vertices]
        return [min(x_coords), max(x_coords), min(y_coords), max(y_coords), min(z_coords), max(z_coords)]


    def generate_scenario(self):
        return json.dumps(self.scenario, indent=2)
    
    def visualize_buildings(self):
        fig, ax = plt.subplots()
        patches = []

        for building in self.scenario['alpha']['buildings']:
            polygon = Polygon(building['vertices'])
            patches.append(polygon)

        p = PatchCollection(patches, alpha=0.4)
        ax.add_collection(p)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_aspect('equal', 'box')
        plt.show()

# Usage example:
area_bounds = (0, 0, 10, 10)
generator = ScenarioGeneratorWithQuadtree(area_bounds)
generator.add_random_buildings(1_000, (0.1, 1.5),1_000_000)
generator.visualize_buildings()

print(len(generator.scenario["alpha"]["buildings"]))
# %%
