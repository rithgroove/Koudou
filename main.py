from src.model.map.map_manager import build_map
from os.path import join 

path = join("osmData","TX-To-TU.osm")
temp = build_map(path)
print(temp)
