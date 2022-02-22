import os
import time
import pandas as pd

class Logger():
    def __init__(self, exp_name):
        self.exp_name = exp_name
        self.path     = f"./results/{exp_name}/{time.time_ns()}"
        self.files    = ["buildings.csv"]

        os.makedirs(self.path, exist_ok=True)
