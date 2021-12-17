from typing import List
from .coordinate import Coordinate


class Render_info:
    def __init__(self, coords: List[Coordinate], centroid: Coordinate, color: str):
        self.coords = coords
        self.center = centroid
        self.color = color
        pass