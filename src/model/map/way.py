class Way():
    """
    [Class] Way
    A class to represent the Open Street Map Way.
       
    Properties:
        - osmId : Open Street Map ID.
        - nodes : List of Nodes included in this way.
        - tags : A dictionary of the Map Feature of this object (check Open Street Map - Map Features).
    """
    
    def __init__(self, osm_id, osm_nodes, osm_tags, our_nodes):
        self.id = osm_id
        
        try:
            self.nodes = [our_nodes[f"n{node.ref}"] for node in osm_nodes]
        except KeyError:
            pass #todo: raise a message in a log file, if possible stating the reason this node is missing (e.g outside simulated area)
        
        self.tags = {tag.k : tag.v for tag in osm_tags}
        
        