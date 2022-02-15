import itertools


class Residence:
    idCounter = itertools.count().__next__

    def __init__(self, node_id: str, road_connection_id: str, max_occupancy: int):
        self.id = self.idCounter()
        self.road_connection_id: str = road_connection_id
        self.node_id: str = node_id

        self.max_occupancy: int = max_occupancy

    def __str__(self):
        tempstring = "[Residence]\n"
        tempstring += f"   ID            : {self.id}\n"
        tempstring += f"   Road Con ID   : {self.road_connection_id}\n"
        tempstring += f"   Node ID       : {self.node_id}\n"
        tempstring += f"   Max occupancy : {self.max_occupancy}\n"
        return tempstring
        