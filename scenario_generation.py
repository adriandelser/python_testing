import json,itertools
import random
import string
from dataclasses import dataclass
from enum import Enum
from typing import Tuple
from geopy.distance import geodesic
import time
from pois import POIs




@dataclass
class Drone:
    model_name: str
    manufacturer: str
    MTOM: int
    tail_number: str
    serial_number: str
    max_endurance: int
    max_speed: int
    max_altitude: int
    EASA_class: str
    aircraft_type: str  # FIXED_WING, MULTI_COPTER, HYBRID
    windspeed_restriction: int  # m/s
    CE_marked: bool
    max_dimension: float  # metres

class DroneType(Enum):
    DJIPHANTOM = Drone('DJI Phantom', 'DJI', 1200, 'T1234', 'S1234', 30, 5, 6000, 'Class 1', 'MULTI_COPTER', 10, True, 0.35)
    # add any other drone types you need


# @dataclass
# class Route:
#     id: int
#     name: str
#     start: str  # POI name
#     end: str  # POI name
#     remarks: str

# class RouteType(Enum):
#     ROUTE1 = Route(1, 'Route 1', 'Capitole de Toulouse', 'Basilique Saint-Sernin', 'No remarks')
#     # add any other route types you need

class MissionType(Enum):
    PIZZA_DELIVERY = 'pizza_delivery'
    MEDEVAC = 'medevac'
    INSPECTION = 'inspection'
    # add any other mission types you need

with open('routes.json','r') as f:
        routes = json.load(f)

def generate_case_file(num_vehicles):
    vehicles = []
    height_intervals = [i for i in range(50, 111, 20)]
    already_flying_ratio = random.uniform(0.15, 0.20)
    still_flying_ratio = random.uniform(0.15, 0.20)
    already_flying_count = round(num_vehicles * already_flying_ratio)
    still_flying_count = round(num_vehicles * still_flying_ratio)

    for i in range(num_vehicles):
        vehicle_id = i
        drone_id = f'HOSP{vehicle_id:03d}'
        auth_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        drone_type = random.choice(list(DroneType)).value
        operator_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        mission_type = random.choice(list(MissionType)).value
        height = random.choice(height_intervals)

        route_key = route_create()
        route = routes[route_key]
        departure_coords, arrival_coords = route['start_coord'], route['end_coord']


        # departure_coords, arrival_coords = route_type.start, route_type.end
        flight_time_seconds = min(25*60, max(10*60, route['length'] 
                                          / drone_type.max_speed))
        # print("length" ,route['length'] , "max speed",drone_type.max_speed, "time sec",route['length'] / drone_type.max_speed)
        flight_start_time = 0 if already_flying_count > 0 else round(random.uniform(0, 3600 - flight_time_seconds))
        flight_end_time = flight_start_time + round(flight_time_seconds) if still_flying_count <= 0 else 3600
        
        if already_flying_count > 0:
            already_flying_count -= 1
        
        if flight_end_time == 3600:
            still_flying_count -= 1
        
        vehicles.append({
            'id': vehicle_id,
            'drone_identifier': drone_id,
            'authorisation_number': auth_number,
            'drone_type': drone_type.model_name,
            'operator_id': operator_id,
            'mission_type': mission_type,
            'height': height,
            'flight_start_time': flight_start_time,
            'flight_end_time': flight_end_time,
            'route': route['name'],
            'departure_POI': route['start'],
            'departure_coordinates': departure_coords,
            'arrival_POI': route['end'],
            'arrival_coordinates': arrival_coords,
            'total_flight_time': flight_time_seconds,
        })
    with open("operations.json","w") as f:
        json.dump(vehicles,f,indent=4)
    return json.dumps(vehicles, indent=4)

def route_create():
    route_key = random.choice(list(routes.keys()))
    # print(route_key)
        # We can calculate the distance between these two points in meters as follows:
        # point1, point2 = POIs[route_type.start], POIs[route_type.end]
        # distance_meters = geodesic(point1, point2).meters
    length = routes[route_key]['length']
    while length < 800:
        # print(length)
        route_key = random.choice(list(routes.keys()))
        length = routes[route_key]['length']
    return route_key



# Test
if __name__ == '__main__':
    generate_case_file(200)






