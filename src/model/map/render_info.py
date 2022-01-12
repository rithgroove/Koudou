from typing import List
from .coordinate import Coordinate


class Render_info:
    def __init__(self, coords: List[Coordinate], centroid: Coordinate, tags: List[str]):
        self.coords = coords
        self.center = centroid
        self.tags = tags

        ## transfer to a config file and then just map it
        #default
        self.outline = '#515464'
        self.fill = '#99CC99'
        if "amenity" in self.tags:
            self.get_color_amenities()
        elif "leisure" in self.tags:
            self.get_color_leisure()
        elif "natural" in self.tags:
            self.get_color_natural()


        type = self.tags.get("building")
        houseType = ["residential","apartments","house"]
        if (type in houseType):
            self.fill = "#99CC99"
        elif (type == "restaurant"):
            self.fill = "#5555DD"
        elif (type == "retail"):
            self.fill = "#DDDD55"

    # temporary functions
    def get_color_amenities(self):
        outline = '#515464'
        fill = '#FF5733'
        if (self.tags['amenity'] == 'school'):
            outline = '#515464'
            fill = '#CCCCCC'
        elif (self.tags['amenity'] == 'police'):
            outline = '#515464'
            fill = '#CCCCCC'
        elif (self.tags['amenity'] == 'karaoke_box'):
            outline = '#515464'
            fill = '#CCCCCC'
        elif (self.tags['amenity'] == 'university'):
            outline = '#619e44'
            fill = '#9edd80'
        elif (self.tags['amenity'] == 'library'):
            outline = '#515464'
            fill = '#CCCCCC'
        elif (self.tags['amenity'] == 'driving_school'):
            outline = '#515464'
            fill = '#CCCCCC'
        elif (self.tags['amenity'] == 'bus_station'):
            outline = '#515464'
            fill = '#CCCCCC'
        elif (self.tags['amenity'] == 'kindergarten'):
            outline = '#515464'
            fill = '#CCCCCC'
        elif (self.tags['amenity'] == 'post_office'):
            outline = '#515464'
            fill = '#CCCCCC'
        elif (self.tags['amenity'] == 'community_centre'):
            outline = '#515464'
            fill = '#CCCCCC'
        elif (self.tags['amenity'] == 'toilets'):
            outline = '#515464'
            fill = '#CCCCCC'
        elif (self.tags['amenity'] == 'bank'):
            outline = '#515464'
            fill = '#CCCCCC'
        elif (self.tags['amenity'] == 'parking'):
            outline = '#515464'
            fill = '#676768'
        elif (self.tags['amenity'] == 'bicycle_parking'):
            outline = '#515464'
            fill = '#676768'
        elif (self.tags['amenity'] == 'parking_space'):
            outline = '#515464'
            fill = '#676768'

        self.outline = outline
        self.fill = fill
    def get_color_leisure(self):
        outline = '#515464'
        fill = '#FF5733'
        if (self.tags['leisure'] == 'park'):
            outline = '#619e44'
            fill = '#9edd80'
        elif (self.tags['leisure'] == 'garden'):
            outline = '#85a22f'
            fill = '#b7da52'
        elif (self.tags['leisure'] == 'track'):
            outline = '#7a651d'
            fill = '#c4a646'
        elif (self.tags['leisure'] == 'pitch'):
            outline = '#7a651d'
            fill = '#c4a646'

        self.outline = outline
        self.fill = fill
    def get_color_natural(self):
        outline = '#515464'
        fill = '#FF5733'
        if (self.tags['natural'] == 'grassland'):
            outline = '#619e44'
            fill = '#9edd80'
        elif (self.tags['natural'] == 'water'):
            outline = '#515464'
            fill = '#8895e4'
        elif (self.tags['natural'] == 'wood'):
            outline = '#2c7509'
            fill = '#42b00d'
        elif (self.tags['natural'] == 'scrub'):
            outline = '#85a22f'
            fill = '#b7da52'
        elif (self.tags['natural'] == 'heath'):
            outline = '#7a651d'
            fill = '#c4a646'

        self.outline = outline
        self.fill = fill
