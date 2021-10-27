from .coordinate import Coordinate
from .way import Way
from .osm_handler import OSMHandler
from .map import Map
from .node import Node
#list of function here

#def connect_buildings

#def clean_up_road

def build_map(path):
	osm_map = OSMHandler()
	osm_map.apply_file(path)
	
	nodes = []
	for n in osm_map.nodes:
		coord = Coordinate(n["location"]["lat"], n["location"]["lon"])
		nodes.append(Node(n["id"], n["tags"], coord))
	
	ways = [Way(w["id"], w["tags"], w["nodes"]) for w in osm_map.ways]
	
	map = Map(nodes, ways)

	return map