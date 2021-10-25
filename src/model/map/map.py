class Map():
    """
    [Class] Map
    A class to represent the map
    
    Properties:
        - origin        : [Coordinate] map's origin coordinate
        - end           : [Coordinate] map's end coordinate
        - num_nodes     : Number of Nodes.
        - nodesDict     : Dictionary of all nodes. The key used are the Open Street Map ID.
        - nodes         : List of all nodes.
        
        - num_ways      : Number of Ways.
        - waysDict      : Dictionary of all nodes. The key used are the Open Street Map ID.
        - ways          : List of all ways.
        
        - num_roads     : Number of Roads.
        - roadNodesDict : 
        - roadNodes     : 
        - roadsDict     : List of all nodes that marked as road.
        - roads         : List of all roads.
        
        - num_buildings : Number of Buildings.
        - buildings     : List of all buildings.
        - naturals      : List of all naturals.
        - leisures      : List of all leisures.
        - amenities     : List of all amenities.
        
        - grids         : [(int,int)] Two dimensional array of grids
        
        - others        : List of other openstreetmap ways that yet to be categorized.
        - gridCellHeight   : height of 1 grid in latitude
        - gridCellWidth   : width of 1 grid in longitude
        - gridsize      : tuple of 2 integer that shows how many grids we have
    """
    def __init__(self,grid = (10,10)):
        """
        [Constructor]    
        Generate Empty Map.
        
        Parameter:
            - grid = grid size, default value = (10,10)
        """
        osmium.SimpleHandler.__init__(self)
        self.origin = Coordinate(0.0,0.0)
        self.end = Coordinate(0.0,0.0)
        
        self.num_nodes = 0
        self.nodesDict = {}
        self.nodes = []
        
        self.num_ways = 0
        self.waysDict = {}
        self.ways = []
        
        self.num_roads = 0
        self.roadNodesDict = {}
        self.roadNodes = []             
        self.roadsDict = {}
        self.roads = []             
        self.num_buildings = 0
        self.buildings = []
        self.buildingsDict = {}
        self.buildingsMap = {}
        
        self.naturals = []
        self.leisures = []
        self.amenities = []
        
        self.grids = [[0 for x in range(grid[1])] for y in range(grid[0])]
        self.others = []
        self.gridCellHeight = None
        self.gridCellWidth = None
        self.gridSize = grid