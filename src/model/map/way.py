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
    
    def __init__(self, osm_id: int, tags: Dict[str, str], nodes: List[int]):
        self.id = str(osm_id)
        self.nodes = [str(n) for n in nodes] #convert the node_id from integer to str
        self.tags = tags
        
    def add_node(self, n_id):
        self.nodes.append(n_id)
        
    def __str__(self):
        """
        [Method] __str__
        Generate the Way information string and return it.
        
        Return: [string] String of summarized map Information.
        """
        temp_string = "[Way]\n"
        temp_string += f"\tid = {self.id}\n"
        temp_string += f"Nodes:\n"
        for x in self.nodes:
            temp_string += f"\t{x}\n"
        temp_string += f"Tags:\n"
        for x in self.tags.keys():
            temp_string += f"\t{x} = {self.tags[x]}\n"
        return(temp_string)
