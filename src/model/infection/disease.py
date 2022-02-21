import json

class Disease:
    def __init__(self, name, attributes, transitions):
        self.name = name
        self.attributes = attributes
        self.transitions = transitions