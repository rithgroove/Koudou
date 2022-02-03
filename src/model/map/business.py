class Business:
    """
    [Class] Business
    A class that represents a business
    """

    def __init__(self, osm_id: int, type: str, working_duration: str):

        self.id = str(osm_id)
        self.type = type
        self.working_duration = working_duration
        self.workers_id = []