from .osm_handler import OSMHandler
from .map import Map
#list of function here

#def connect_buildings

#def clean_up_road

def build_map(path):
	osm_map = OSMHandler()
	osm_map.apply_file(path)
	map = Map()
	# Add function that translates osm_map to map here
	return map