import itertools

from .render_info import Render_info

class Place:
    """
    [Class] Place
    A class to a structure on the map, it can be a building, a supermarket, a statue, ...
    """
    idCounter = itertools.count().__next__

    def __init__(self, osm_id: int, interactable: bool, render_info: Render_info, centroid_id: str, road_connection_id: str):
        
        self.id = str(osm_id)
        self.interactable = interactable
        self.render_info = render_info
        self.centroid = centroid_id
        self.road_connection = road_connection_id

        self.type = None
        self.evacuation_attr = None
        self.evacuation_center = False
