from src.model.map.coordinate import Coordinate
class Node:
    """
    [Class] Node
    A class to represent the Open Street Map Node.
    
    Properties:
        - osmId             : Open Street Map ID.
        - coordinate        : coordinate 
        - isRoad            : Boolean to mark whether this Node is a part of a road.
        - connection        : List of all connected node.
        - ways              : A dictionary of Open Street Map Ways.
        - tags              : A dictionary of the Map Feature of this object (check Open Street Map - Map Features).
        - grid              : [Grid] The grid this node is in
        - movementSequences : [MovementSequence] Dictionary of previously generated movementSequences destination id is the key
        - agents            : [Agents] agents in this node (might replace it later with something)
    """    
    def __init__(self):
        """
        [Constructor]
        Initialize an empty node.
        """
        self.osmId = ""
        self.hashId = 0
        self.coordinate = Coordinate(0.0,0.0)
        self.isRoad = False
        self.connections = []
        self.ways = {}
        self.tags = {}
        #self.grid = None
        #self.isBuildingCentroid = False
        #self.building = None
        
    def fill(self, osmNode):
        """
        [Method]fill        
        Fill up several property of this object, such as:
            - osmId
            - coordinate
            - isRoad
            - tags
        
        Parameter:
            - osmNode = List of osmium library node.
        """
        self.osmId = f"{osmNode.id}"
        self.coordinate = Coordinate(osmNode.location.lat,osmNode.location.lon)
        for tag in osmNode.tags:
            self.tags[tag.k] = tag.v
        if 'highway' in self.tags.keys():
            self.isRoad = True
        #self.generateHashId()
            
