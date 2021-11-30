from .place import Place
from .render_info import Render_info
from .coordinate import Coordinate
from .way import Way
from .osm_handler import OSMHandler
from .map import Map
from .node import Node
from typing import List
#list of function here

#def connect_buildings

#def clean_up_road

def build_map(path):
	osm_map = OSMHandler()
	osm_map.apply_file(path)
	osm_map.set_bounding_box(path)

	nodes = []
	for n in osm_map.nodes:
		coord = Coordinate(n["location"]["lat"], n["location"]["lon"])
		tags = {t[0]: t[1] for t in n["tags"]}
		nodes.append(Node(n["id"], tags, coord))

	ways = []
	for w in osm_map.ways:
		tags = {t[0]: t[1] for t in w["tags"]}
		n = [n["ref"] for  n in w["nodes"]]
		ways.append(Way(w["id"], tags, n))

	kd_map = Map(osm_map.bounding_box, nodes, ways)
	build_node_connections(kd_map) #generate the connection between nodes

	road_nodes, non_road_nodes = separate_nodes(kd_map)	# separate road and other nodes
	main_road_graph, disconnected_nodes = clean_road(road_nodes,kd_map) # separate the road_graph and disconnected nodes

	kd_map.set_main_road(main_road_graph)

	places = create_places_osm(ways, kd_map, main_road_graph)

	businesses, households = create_types_osm_csv(places, ways)

	repair_places(places, businesses, households)

	return kd_map


def create_places_osm(ways, kd_map, main_road_graph, grid_size):
	places = {}
	road_grid = create_roades_grid(kd_map, main_road_graph, grid_size)
	for w in ways:
		if 'road' in w.tags:
			continue
		
		centroid = create_centroid(w, kd_map.d_nodes)
		kd_map.add_node(centroid)

		centroid_grid_coord = get_node_grid_coordinate(centroid, kd_map, grid_size)
		road_connection = create_road_connection(centroid, centroid_grid_coord, road_grid)
		
		render_info = Render_info()
		p = Place(w.id, True, render_info, centroid.id, road_connection)
		places[p.id] = p

	return places

def create_centroid(way, n_dict):
	lat, lon = 0, 0
	for n_id in way.nodes:
		lat += n_dict[n_id].coordinate.lat
		lon += n_dict[n_id].coordinate.lon

	size = len(way.nodes)-1
	coord = Coordinate(lat/size, lon/size)
	new_id = n_dict[way.nodes[-1]].id + "_c"
	n = Node(new_id, {"centroid": True}, coord)
	return n


def get_node_grid_coordinate(node, kd_map, grid_size):
	cell_height = (kd_map.max_lon - kd_map.min_lon)/grid_size
	cell_width = (kd_map.max_lon - kd_map.min_lon)/grid_size

	x = int((node.coordinate.lon - kd_map.min_lon) / cell_width)
	y = int((node.coordinate.lat - kd_map.min_lat) / cell_height)

	return (x, y)

def create_road_connection(centroid, centroid_grid_coord, road_grid):
	x = centroid_grid_coord[0]
	y = centroid_grid_coord[1]

	visited_roads = {{}}
	for node1 in road_grid[x][y]:
		for node2 in node1.connections:
			if node1 in visited_roads and node2 in visited_roads[node1]:
				continue
			visited_roads[node1][node2] = True
			# dist = node_road_dist(centroid, node1, node2)		

def create_types_osm_csv (places, ways, csv_file_name):
	# file = open(csv_file_name)
	# for line in file:
	# for w in ways:
	# 		if 'ammenity' in w.tags:
	# 			b = Business(places[w.id])
	# 		if 'building' in w.tags and w.tags['building'] == 'restaurant':
	# 			b = Business(places[w.id], type='restaurant')
	# 		if 'building' in w.tags and w.tags['building'] == 'apartament':
	# 			h = Household(places[w.id])
	# 		if not_interactable:
	# 			places[w.id].interactable = False


	# return households,businesses
	pass


def repair_places():
	pass

def build_node_connections(kd_map):
	for key in kd_map.d_ways:
		way = kd_map.d_ways[key]
		working_node = None
		for node_id in way.nodes:
			if working_node is not None:
				connectingNode = kd_map.d_nodes[node_id] 
				working_node.addConnection(node_id) #add the connection from working_node to the connecting_node
				connectingNode.addConnection(working_node.id) #add the connection from the connecting_node to the working_node
			working_node = kd_map.d_nodes[node_id]

def separate_nodes(kd_map):
	road_nodes = []
	other_nodes = []
	for key in kd_map.d_nodes:
		node = kd_map.d_nodes[key]
		if (node.is_road):
			road_nodes.append(node)
		else:
			other_nodes.append(node)
	return road_nodes, other_nodes

def clean_road(road_nodes, kd_map):
	working_node = None
	results = []
	while len(road_nodes)>0: #loop until road_nodes empty
		queue = [road_nodes[0]] #put 1 starting nodes to the queue
		visited = []
		while len(queue) > 0: #loop until queue is empty
			working_node = queue.pop(0) #pop the queue
			if (working_node in road_nodes): road_nodes.remove(working_node) #remove the working_node from road_nodes
			visited.append(working_node) #add the node to the visited
			for node_id in working_node.connections:
				node = kd_map.d_nodes[node_id] #get the node
				if (node not in visited and node not in queue):
					queue.append(node) #if the node never visited, put it on queue
		results.append(visited) #append all of the visited road as 1 graph

	main_road = []
	disconnected_nodes = []
	largest = 0
	for result in results:
		if (len(result)>largest):
			disconnected_nodes.extend(main_road)
			largest = len(result)
			main_road = result
		else:
			disconnected_nodes.extend(result)
			
	return main_road, disconnected_nodes


def create_roades_grid(kd_map, road_nodes, grid_size: int):
	grid = []
	for i in range(grid_size):
		grid.append([])
		for _ in range(grid_size):
			grid[i].append([])

	for n in road_nodes:
		x, y = get_node_grid_coordinate(n, kd_map, grid_size)
		grid[x][y].append(n.id)

	return grid
