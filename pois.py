import json,itertools
from dataclasses import dataclass
from geopy.distance import geodesic
# from scenario_generation import Route
from dataclasses import asdict
import time
from unidecode import unidecode


from geopy.geocoders import Nominatim

POIs = {
    'Capitole': (43.6043, 1.4437),  # Capitole de Toulouse
    'StSernin': (43.6049, 1.4442),  # Basilique Saint-Sernin
    'CiteEspc': (43.5893, 1.4946),  # Cité de l’espace
    'AugMuse': (43.5978, 1.4399),   # Musée des Augustins
    'CanMidi': (43.6058, 1.4348),   # Canal du Midi
    'AeroMus': (43.6636, 1.3648),   # Musée Aeroscopia
    'PontNeuf': (43.6040, 1.4443),  # Pont Neuf, Toulouse
    'PlCapitl': (43.6045, 1.4440),  # Place du Capitole
    'JardPlan': (43.6085, 1.4580),  # Jardin des Plantes, Toulouse
    'JardJapn': (43.6130, 1.4330),  # Jardin Japonais, Toulouse
    'StRayMus': (43.6090, 1.4420),  # Musée Saint-Raymond
    'PraFilts': (43.5940, 1.4420),  # Prairie des Filtres
    'PlStPier': (43.6030, 1.4430),  # Place Saint-Pierre, Toulouse
    'ChateauEa': (43.6000, 1.4440),  # Le Château d’Eau, Toulouse
    'HotelAssz': (43.6020, 1.4400),  # Hôtel d’Assézat
    'BasiDaur': (43.6010, 1.4450),  # Basilique de la Daurade
    'CentAffch': (43.5980, 1.4450),  # Centre de l’affiche, Toulouse
    'MuseTouls': (43.5920, 1.4420),  # Muséum de Toulouse
    'CouvJaco': (43.6070, 1.4410),  # Couvent des Jacobins, Toulouse
    'HalleGrns': (43.6110, 1.4540),  # Halle aux grains, Toulouse
}

short_names = {
    'Capitole de Toulouse': 'Capitole',
    'Basilique Saint-Sernin': 'StSernin',
    'Cité de l’espace': 'CiteEspc',
    'Musée des Augustins': 'AugMuse',
    'Canal du Midi': 'CanMidi',
    'Musée Aeroscopia': 'AeroMus',
    'Pont Neuf, Toulouse': 'PontNeuf',
    'Place du Capitole': 'PlCapitl',
    'Jardin des Plantes, Toulouse': 'JardPlan',
    'Jardin Japonais, Toulouse': 'JardJapn',
    'Musée Saint-Raymond': 'StRayMus',
    'Prairie des Filtres': 'PraFilts',
    'Place Saint-Pierre, Toulouse': 'PlStPier',
    'Le Château d’Eau, Toulouse': 'ChateauEa',
    'Hôtel d’Assézat': 'HotelAssz',
    'Basilique de la Daurade': 'BasiDaur',
    'Centre de l’affiche, Toulouse': 'CentAffch',
    'Muséum de Toulouse': 'MuseTouls',
    'Couvent des Jacobins, Toulouse': 'CouvJaco',
    'Halle aux grains, Toulouse': 'HalleGrns'
}

long_names = {v: unidecode(k) for k, v in short_names.items()}

POIdict = {}
for idx, key in enumerate(POIs.keys()):
    long_name = long_names[key]
    POIdict[key] = [{"ID": idx, 'short_name':key,"name": long_name, "coords": POIs[key]}]

with open("poi.json", "w") as f:
    json.dump(POIdict, f, indent=4)

# def get_coordinates(place_name):
#     geolocator = Nominatim(user_agent="myGeocoder")
#     location = geolocator.geocode(place_name)
#     if location:
#         # print(location)
#         return location.latitude, location.longitude
#     else:
#         return None, None

# latitude, longitude = get_coordinates('Capitole de Toulouse')
# print(f'Coordinates of Capitole de Toulouse are {latitude}, {longitude}')

# names = POIs.keys()
# for name in names:
#     latitude, longitude = get_coordinates(name)
#     print(f'Coordinates of {name}, Toulouse are {latitude}, {longitude}')
    # POIs[name] = (latitude,longitude)

# for name,coords in POIs.items():
#     latitude, longitude = get_coordinates(f"{name}, France'")
#     print(name, latitude, longitude)
#     time.sleep(2)
    # if latitude:
    #     print(name, latitude, longitude)
    #     POIs[name] = (latitude,longitude)

# print(POIs)




@dataclass
class Route:
    id: int
    name: str
    length:float
    start: str  # POI name
    start_coord: tuple
    end: str  # POI name
    end_coord: tuple
    remarks: str

all_pois = list(POIs.keys())
valid_routes = {}
route_id = 0

# Generate all possible combinations of two different POIs
for start, end in itertools.combinations(all_pois, 2):
    #print(start)
    distance = geodesic(POIs[start], POIs[end]).meters
    route_name = f"{start} --> {end}"
    if distance >= 800:
        route = Route(route_id, f"{route_name}",round(distance,1), start, POIs[start],end,POIs[end], "No remarks")
        valid_routes[f"R{route.id}"]=asdict(route)  # Convert to dictionary to be able to serialize it
        route_id += 1

# Save to JSON file
with open("routes.json", "w") as f:
    json.dump(valid_routes, f, indent=4)