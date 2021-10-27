from typing import Dict, List
from .coordinate import Coordinate

class Node():
    """
    [Class] Node
    A class to represent the Open Street Map Node.
    
    Properties:
        - id                : (int) same as Open Street Map ID.
        - coordinate        : (Coordinate) coordinate(lat, lon)
        - is_road           : (boolean) True if part of a road
        - tags              : (dict) of the Map Feature of this object (check Open Street Map - Map Features).
    """    
    def __init__(self, osm_id: int, osm_tags: List, location: Coordinate):
        """
        [Constructor]
        Initialize a node
        """
        self.id = str(osm_id) 
        self.coordinate = location
        self.tags = {}
        for t in osm_tags:
            self.tags[t[0]] = t[1]
        self.is_road = True if 'highway' in self.tags.keys() else False

        