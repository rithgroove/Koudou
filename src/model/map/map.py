from typing import Dict, List

from .node import Node
from .way import Way


class Map():
    def __init__(self, nodes: List[Node], ways: List[Way]):
        self.d_nodes: Dict[str, Node] = {}
        self.d_ways: Dict[str, Way] = {}

        for node in nodes:
            self.d_nodes[node.id] = node

        for way in ways:
            self.d_ways[way.id] = way