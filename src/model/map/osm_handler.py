import datetime
import osmium


class OSMHandler(osmium.SimpleHandler):
    def __init__(self):
        osmium.SimpleHandler.__init__(self)

        self.nodes = []
        self.ways  = []

    def obj_to_dict(self, obj):
        values = {}
        for k in [name for name in dir(obj) if not name.startswith('__')]:
            v = getattr(obj, k)
            if not callable(v):
                if not isinstance(v, (int, float, str, bool, datetime.datetime)):
                    if isinstance(v, osmium.osm.TagList):
                        v = {tag.k : tag.v for tag in v}
                    else:
                        v = self.obj_to_dict(v)
                values[k] = v
        return values

    def node(self, osm_node):
        self.nodes.append(self.obj_to_dict(osm_node))

    def way(self, osm_way):
        self.ways.append(self.obj_to_dict(osm_way))
