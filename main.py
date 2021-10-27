import osmium
from src.model.map.map_manager import build_map
from os.path import join 

osm_file = join("osm_files","TX-To-TU.osm")

map = build_map(osm_file)

print(map)


