from typing import Dict, List


class Way():
    """
    [Class] Way
    A class to represent the Open Street Map Way.
       
    Properties:
        - osmId : Open Street Map ID.
        - nodes : List of Nodes included in this way.
        - tags : A dictionary of the Map Feature of this object (check Open Street Map - Map Features).
    """
    
    def __init__(self, osm_id: int, osm_tags: List, nodes: List):
        self.id = str(osm_id)
        self.nodes = [n["ref"] for  n in nodes]
        self.tags = {}
        for t in osm_tags:
            self.tags[t[0]] = t[1]
        