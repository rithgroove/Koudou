from .coordinate import Coordinate


class Render_info:
    def __init__(self, coord: Coordinate, color: str):
        self.coord = coord
        self.color = color
        pass