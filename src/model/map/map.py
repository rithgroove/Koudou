from typing import Dict, List

from .node import Node
from .way import Way


class Map():
    def __init__(self, nodes: List[Node], ways: List[Way], boundingBox = None):
        self.d_nodes: Dict[str, Node] = {}
        self.d_ways: Dict[str, Way] = {}

        for node in nodes:
            self.d_nodes[node.id] = node

        for way in ways:
            self.d_ways[way.id] = way

        if (boundingBox is not None):
            self.minLat = boundingBox.bottom_left.lat
            self.minLon = boundingBox.bottom_left.lon
            self.maxLat = boundingBox.top_right.lat
            self.maxLon = boundingBox.top_right.lon
        else:
            self.minLat = 0
            self.minLon = 0
            self.maxLat = 0
            self.maxLon = 0