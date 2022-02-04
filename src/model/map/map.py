import time
from tracemalloc import start
from typing import Any, Dict, List, Tuple
import numpy as np

from .road import Road

from .place import Place
from .node import Node
from .way import Way
from .coordinate import Coordinate
from .a_star import a_star_search, parallel_a_star

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

    def test_a_star(self, n_tests):
        t = time.time()
        for i in range(n_tests):
            start = np.random.choice(self.main_road)
            goal = np.random.choice(self.main_road)
            path = a_star_search(self, start.id, goal.id)
            if i%100 == 0:
                print(i)
        print(f"{n_tests} tests: {time.time()-t}s")

    def test_parallel_a_star(self, n_tests, n_threads):
        paths = []
        for _ in range(n_tests):
            start = np.random.choice(self.main_road)
            goal = np.random.choice(self.main_road)
            paths.append((start.id, goal.id))

        t = time.time()
        res = parallel_a_star(self, paths, n_threads, 100)
        print(f"{n_tests} tests in {n_threads} threads: {time.time()-t}s")
