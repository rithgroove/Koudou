from collections import OrderedDict
import parameters.default as defaultParam
from .utils import *

# ---------------- App ------------------
# BS = 'https://bootswatch.com/5/lumen/bootstrap.min.css'
# BS = 'https://bootswatch.com/5/sketchy/bootstrap.min.css'
# BS = 'https://bootswatch.com/5/flatly/bootstrap.min.css'
BS = 'https://bootswatch.com/5/united/bootstrap.min.css'
# BS = ''

# ---------------- config ------------------
data_default_config = OrderedDict(
    [
        (
            "Parameter",
            ["SEED",
             "N_AGENTS",
             "THREADS",
             "GRID_SIZE",
             "STEP_LENGTH",
             "MAX_STEPS",
             "EVACUATION.SHARE_INFO_CHANCE",
             "EVACUATION.DISTANCE",
             ],
        ),
        (
            "Value",
            [str(defaultParam.parameters.get("SEED")),
             str(defaultParam.parameters.get("N_AGENTS")),
             str(defaultParam.parameters.get("THREADS")),
             str(defaultParam.parameters.get("GRID_SIZE")),
             str(defaultParam.parameters.get("STEP_LENGTH")),
             timestamp_converter(defaultParam.parameters.get("MAX_STEPS")),
             str(defaultParam.parameters.get("EVACUATION").get("SHARE_INFO_CHANCE")),
             str(defaultParam.parameters.get("EVACUATION").get("DISTANCE")),
             ],
        ),
        (
            "Description",
            ["Used for reproducing experiments",
             "Number of agents in the simulation",
             "Number of CPUs be used for pathfinding",
             "Used when calculating the centroid for buildings",
             "Each step is one second",
             "Simulation duration for one cycle",
             "Agents have 80% chance of sharing information",
             "if they have a distance less than 10"
             ]
        ),
    ]
)

default_config_df = pd.DataFrame(data_default_config)


# ---------------- infection ------------------
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://codepen.io/chriddyp/pen/brPBPO.css']