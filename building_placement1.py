#%%
import random
from rtree import index
import json
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
import numpy as np
from shapely.geometry import Point



class ScenarioGenerator:
    def __init__(self, name):
        self.name = name
        self.scenario = {self.name: {"buildings": [], "vehicles": []}}
        self.building_index = index.Index()

    def add_random_buildings(self, n, building_size_range, area_bounds, max_attempts=1000):
        placed_buildings = 0
        failed_attempts = 0

        # If max_buildings is not specified, use the provided n value
        # max_buildings = max_buildings if max_buildings is not None else n

        for _ in range(n):
            # if placed_buildings >= max_buildings:
            #     break

            added = False
            while not added and failed_attempts < max_attempts:
                size = random.uniform(*building_size_range)
                x = random.uniform(area_bounds[0], area_bounds[2] - size)
                y = random.uniform(area_bounds[1], area_bounds[3] - size)
                if not self.check_overlap(x, y, size):
                    self.add_building(x, y, size)
                    placed_buildings += 1
                    failed_attempts = 0
                    added = True
                else:
                    failed_attempts += 1

            if failed_attempts >= max_attempts:
                print(f"Stopped after {failed_attempts} failed attempts to place a building.")
                break


    def add_building(self, x, y, size):
        building_id = len(self.scenario[self.name]['buildings'])
        vertices = [[x, y], [x + size, y], [x + size, y + size], [x, y + size]]
        self.scenario[self.name]['buildings'].append({"ID": f"Building {building_id}", "vertices": [vertex + [1.2] for vertex in vertices]})
        self.building_index.insert(building_id, (x, y, x + size, y + size))

    # ... Other methods ...

    def check_overlap(self, x, y, size):
        return list(self.building_index.intersection((x, y, x + size, y + size)))
    

    def add_vehicle(self, position, goal):
        vehicle_id = f"V{len(self.scenario[self.name]['vehicles']) + 1}"
        vehicle = {
            "ID": vehicle_id,
            "position": list(position) + [0.5],
            "goal": list(goal) +[0.5],
            "source_strength": 1,
            "imag_source_strength": 0.5,
            "sink_strength": 5,
            "safety": 0.0001
        }
        self.scenario[self.name]['vehicles'].append(vehicle)

    
    def calculate_bounding_box(self, vertices):
        x_coords = [v[0] for v in vertices]
        y_coords = [v[1] for v in vertices]
        z_coords = [v[2] for v in vertices]
        return [min(x_coords), max(x_coords), min(y_coords), max(y_coords), min(z_coords), max(z_coords)]


    def add_random_vehicles(self,n, area_bounds, min_distance):
        # vehicles = []
        for _ in range(n):
            position, goal = None, None

            # Find a valid position
            while not position:
                candidate_position = self.generate_random_point(area_bounds)
                point = Point(candidate_position)
                bbox = (point.x, point.y, point.x, point.y)
                if not list(self.building_index.intersection(bbox)):
                    position = candidate_position

            # Find a valid goal
            while not goal:
                candidate_goal = self.generate_random_point(area_bounds)
                point = Point(candidate_goal)
                bbox = (point.x, point.y, point.x, point.y)
                if not list(self.building_index.intersection(bbox)) and self.distance(position, candidate_goal) >= min_distance:
                    goal = candidate_goal

            # vehicles.append({'position': position, 'goal': goal})
            self.add_vehicle(position, goal)

        return None

    def generate_random_point(self,bounds):
        x = random.uniform(bounds[0], bounds[2])
        y = random.uniform(bounds[1], bounds[3])
        return (x, y)

    def distance(self,point1, point2):
        return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)



    def generate_scenario(self):
        return json.dumps(self.scenario, indent=2)
    
    
    def visualize_buildings(self):
        fig, ax = plt.subplots()
        patches = []

        for building in self.scenario[self.name]['buildings']:
            polygon = Polygon(building['vertices'])
            patches.append(polygon)

        p = PatchCollection(patches, alpha=0.4)
        ax.add_collection(p)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_aspect('equal', 'box')
        plt.show()

# Usage example:
generator = ScenarioGenerator("large_case")
# generator.name = "large_case"

bounds = (-100, -100, 100, 100)
generator.add_random_buildings(10_000, (0.5, 1), bounds, 10_000)  # Add 10 buildings with sizes between 0.5 and 1.5 in a 10x10 area
generator.add_random_vehicles(40, bounds, min_distance=0.5)  # Add 3 vehicles in a 10x10 area
# print(generator.generate_scenario())
# print(generator.building_index.properties)
# print(len(generator.building_index))
path = "/Users/adriandelser/Desktop/ENAC/gflow/examples/large_case.json"
json.dump(generator.scenario, open(path, "w"),indent=4)
# from shapely.geometry import Point
# point = Point(5,5)
# bbox = (point.x, point.y, point.x, point.y)  # Bounding box for the point
# potential_obstacles_ids = list(generator.building_index.intersection(bbox))

# print(f"{potential_obstacles_ids=}")

# generator.visualize_buildings()



# %%
