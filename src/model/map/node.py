from typing import Dict, List, Union
from .coordinate import Coordinate

class Node():
    """
    [Class] Node
    A class to represent the Open Street Map Node.
    
    Properties:
        - id                : (int or str) same as Open Street Map ID.
        - coordinate        : (Coordinate) coordinate(lat, lon)
        - is_road           : (boolean) True if part of a road
        - tags              : (dict) of the Map Feature of this object (check Open Street Map - Map Features).
    """    
    def __init__(self, osm_id: Union[int, str], tags: Dict[str, str], location: Coordinate):
        """
        [Constructor]
        Initialize a node
        """
        self.id = str(osm_id) 
        self.coordinate = location
        self.tags = tags
        self.is_road = True if 'highway' in self.tags.keys() else False
        self.connections: List[str] = []

    def __str__(self):
        """
        [Method] __str__
        Generate the Node information string and return it.
        
        Return: [string] String of summarized map Information.
        """
        temp_string = "[Node]\n"
        temp_string += f"\tid = {self.id}\n"
        temp_string += f"{self.coordinate.__str__()}\n"
        if len(self.tags) > 0:
            temp_string += "Tags:\n"
            for key in self.tags:
                temp_string += f"\t{key} = {self.tags[key]}\n"
        if len(self.connections) > 0:
            temp_string += "Connection:\n"
            for connection in self.connections:
                temp_string += f"\t{connection}\n"
        return(temp_string)

    def addConnection(self, node_osm_id):
        if (node_osm_id not in self.connections):
            self.connections.append(node_osm_id)