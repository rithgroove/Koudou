from src.model.behavioral import agent_manager

class Simulation:
	def __init__(self,config,rng,agents_count):
		self.agents = []
		attribute_generator = agent_manager.load_attributes_generator(config["attribute_generator"],rng)
		self.agents = agent_manager.generate_agents(attribute_generator,agents_count)		
		self.conditions = agent_manager.load_conditions(config["condition"])
		self.rng = rng

	def __str__(self):
		tempstring = "[Simulation]\n"
		tempstring += f"Total agents = {len(self.agents)}\n"
		tempstring += f"Condition = {len(self.conditions)}\n"
		return tempstring

	def test(self):
		for x in self.agents:

			print(x)