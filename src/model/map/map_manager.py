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
	kd_map = Map(nodes, ways)
	build_node_connections(kd_map) #generate the connection between nodes

	road_nodes,other_nodes = separate_nodes(kd_map)	# separate road and other nodes
	main_road,disconnected_nodes = clean_road(road_nodes,kd_map) # separate the main_road and disconnected nodes

	kd_map.set_main_road(main_road)

	return kd_map

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
	return road_nodes,other_nodes

def clean_road(road_nodes,kd_map):
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
	return main_road,disconnected_nodes
