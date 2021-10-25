from src.model.map.map_handler import MapHandler
#list of function here

#def connect_buildings

#def clean_up_road

def build_map(path):
	osm_map = MapHandler()
	osm_map.apply_file(path)
	return osm_map