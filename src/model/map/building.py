from model.map.way import Way
from .coordinate import Coordinate
import itertools

class Building:
    """
    [Class] Building
    A class to represent the Building
    
    Properties:
        - way: List of nodes that defines the shape of the building.
        - coordinate : the coordinate of the building's centroid
    """
    idCounter = itertools.count().__next__
    def __init__(self, way: Way):
        """
        [Constructor]
        Initialize the building building

        Parameter:
            - way: [Way] the building outline from Open Street Map
        """
        self.buildingId = self.idCounter()
        self.way = way
        lat,lon = 0,0
        for node in way.nodes[:-1]:
            lat += node.coordinate.lat
            lon += node.coordinate.lon
        lat = lat/(way.nodes.__len__()-1)
        lon = lon/(way.nodes.__len__()-1)
        self.coordinate = Coordinate(lat,lon)
        self.closestRoad = None
        self.entryPoint = None
        self.entryPointNode = None
        self.tags = way.tags
        self.setType(self.tags.get("building"))
        if self.type == "yes" and "amenity" in self.tags.keys():
            self.setType(self.tags.get("amenity"))
        self.node = None
        self.content = {}
        self.visitHistory = {}
        active = False