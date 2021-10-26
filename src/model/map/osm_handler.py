import osmium
from .node import Node
from .way  import Way

class OSMHandler(osmium.SimpleHandler):
    def __init__(self):
        osmium.SimpleHandler.__init__(self)
        
        self.d_nodes = {}
        self.d_ways  = {}
        
    def node(self, osm_node):
        new_node = Node(osm_node.id, osm_node.location, osm_node.tags)
        self.d_nodes[new_node.id] = new_node
        
    def way(self, osm_way):
        new_way = Way(osm_way.id, osm_way.nodes, osm_way.tags, our_nodes=self.d_nodes)
        self.d_ways[new_way.id] = new_way
        