from src.model.behavioral.module import Module
from src.model.infection.infection_manager import initialize_infection, infection_step
class InfectionModule(Module):

	def __init__(self, parameters, kd_sim,rng):
		self.infection = initialize_infection(parameters["DISEASES"], kd_sim.agents, rng)

	def step(self,kd_sim,kd_map,ts,step_length,rng,logger):
	    infection_step(step_length, kd_map, kd_sim.agents, self.infection, rng,logger,ts)
