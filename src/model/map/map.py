from typing import Any, Dict, List

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

        self.min_lat = bounding_box.bottom_left.lat
        self.min_lon = bounding_box.bottom_left.lon
        self.max_lat = bounding_box.top_right.lat
        self.max_lon = bounding_box.top_right.lon

        self.min = Coordinate(self.min_lat, self.min_lon)
        self.max = Coordinate(self.max_lat, self.max_lon)

        self.d_places: Dict[str, Place] = {}

    def add_node(self, node):
        self.d_nodes[node.id] = node

    def add_way(self, way):
        self.d_ways[way.id] = way

    def add_place(self, place):
        self.d_places[place.id] = place

    def __str__(self):
        tempstring = "[Map]\n"
        tempstring += f"Simulated area = ({self.min_lon},{self.min_lat}) to ({self.max_lon},{self.max_lat})\n"
        tempstring += f"Number of nodes = {len(self.d_nodes)}\n"
        tempstring += f"Number of ways = {len(self.d_ways)}"
        return tempstring

    def set_main_road(self, main_road):
        self.main_road = main_road
