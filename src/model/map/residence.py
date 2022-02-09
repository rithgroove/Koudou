import itertools


class Residence:
    idCounter = itertools.count().__next__

    def __init__(self, node_id: str, road_connection_id: str, max_occupancy: int):
        self.id = self.idCounter()
        self.road_connection_id: str = road_connection_id
        self.node_id: str = node_id

        self.max_occupancy: int = max_occupancy
        