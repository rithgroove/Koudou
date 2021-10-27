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
    
    def __init__(self, osm_id: int, tags: Dict[str, str], nodes: List):
        self.id = str(osm_id)
        self.nodes = nodes
        self.tags = tags
        