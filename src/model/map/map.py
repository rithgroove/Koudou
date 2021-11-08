from typing import Dict, List

from .node import Node
from .way import Way


class Map():
    def __init__(self,bounding_box, nodes: List[Node], ways: List[Way]):
        self.d_nodes: Dict[str, Node] = {}
        self.d_ways: Dict[str, Way] = {}

        for node in nodes:
            self.d_nodes[node.id] = node

        for way in ways:
            self.d_ways[way.id] = way

        if (bounding_box is not None):
            self.min_lat = bounding_box.bottom_left.lat
            self.min_lon = bounding_box.bottom_left.lon
            self.max_lat = bounding_box.top_right.lat
            self.max_lon = bounding_box.top_right.lon
        else:
            self.min_lat = 0
            self.min_lon = 0
            self.max_lat = 0
            self.max_lon = 0

    def __str__(self):
        tempstring = "[Map]\n"
        tempstring += f"Simulated area = ({self.min_lon},{self.min_lat}) to ({self.max_lon},{self.max_lat})\n"
        tempstring += f"Number of nodes = {len(self.d_nodes)}\n"
        tempstring += f"Number of ways = {len(self.d_ways)}"
        return tempstring