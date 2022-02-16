from typing import Any, Dict, List, Tuple
from .residence import Residence
from .business import Business
from .road import Road
from .place import Place
from .node import Node
from .way import Way
from .coordinate import Coordinate

class Map():
    def __init__(self, bounding_box: Any, nodes: List[Node], ways: List[Way]):
        self.d_nodes: Dict[str, Node] = {}
        self.d_ways: Dict[str, Way] = {}
        self.main_road: List[Node] = []
        for node in nodes:
            self.d_nodes[node.id] = node

        for way in ways:
            self.d_ways[way.id] = way

        self.min_coord = Coordinate(bounding_box.bottom_left.lat, bounding_box.bottom_left.lon)
        self.max_coord = Coordinate(bounding_box.top_right.lat, bounding_box.top_right.lon)

        self.d_places: Dict[str, Place] = {}
        self.d_roads: Dict[Tuple[str, str], Road] = {} # the tuple of id is ordered, NOT start, goal
        self.d_businesses: Dict[str, Business] = {}
        self.d_residences: Dict[str, Residence] = {}

    def add_node(self, node):
        self.d_nodes[node.id] = node

    def add_way(self, way):
        self.d_ways[way.id] = way

    def add_place(self, place):
        self.d_places[place.id] = place

    def add_road(self, road):
        t = (road.start_id, road.goal_id)
        self.d_roads[t] = road

    def remove_road(self, start_id, goal_id):
        del self.d_roads[(start_id, goal_id)]

    def __str__(self):
        tempstring = "[Map]\n"
        tempstring += f"Simulated area = ({self.min_coord.lon},{self.min_coord.lat}) to ({self.max_coord.lon},{self.max_coord.lat})\n"
        tempstring += f"Number of nodes = {len(self.d_nodes)}\n"
        tempstring += f"Number of ways = {len(self.d_ways)}"
        return tempstring

    def set_main_road(self, main_road):
        self.main_road = main_road

    def get_random_business(self, business_type, qtd, rng, time_stamp=None, only_open=False, only_closed=False):
        arr = [b for b in self.d_businesses.values()]
        if only_open:
            arr = [b for b in arr if b.is_open(time_stamp)]
        elif only_closed:
            arr = [b for b in arr if not b.is_open(time_stamp)]

        arr = [b for b in arr if b.type == business_type]
        
        results = rng.choice(arr, qtd, replace=False)
        return results
