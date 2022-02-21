import json
from typing import Dict, List
from .disease import Disease

class Infection:
    def __init__(self, diseases: List[Disease]):
        self.diseases: Dict[str, Disease] = {}
        for d in diseases:
            self.diseases[d.name] = d

                