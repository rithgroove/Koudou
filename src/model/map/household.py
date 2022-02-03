import random

class Household:
    """
    [Class] Household
    A class that represents a household
    """

    def __init__(self, osm_id: int):

        self.id = str(osm_id)
        self.max_occupancy = random.randint(2,8)
        self.residents_id = []