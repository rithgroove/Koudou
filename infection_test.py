from src.utils.parser import load_parameters
from src.model.behavioral.simulation import Simulation
from src.model.infection.infection_manager import initialize_infection, infection_step
import pickle
import numpy as np

parameters = load_parameters("parameters/default.py")
with open("cache/TX-To-TU.pkl", "rb") as file:
    kd_map = pickle.load(file)

rng = np.random.default_rng(seed=101512)
agents_count = 4

sim = Simulation(parameters["SIM_CONFIG"], kd_map, rng, 100, threads=2)
infection = initialize_infection(parameters["DISEASES"], sim.agents, rng)

print(sim)
print("#####################################################################")

day = 1 * 24
step_size = 3600

for x in range(0, day):
    infection_step(step_size, kd_map, sim.agents, infection, rng)
    sim.step(step_size)
