import itertools

class Road:
    idCounter = itertools.count().__next__

    def __init__(self, start_id: str, goal_id: str, distance: float):
        self.id = self.idCounter()

        self.start_id = start_id
        self.goal_id = goal_id

        self.length = distance

        self.one_way = False # This si not used right now

