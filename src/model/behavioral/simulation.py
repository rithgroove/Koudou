from src.model.behavioral import agent_manager

class Simulation:
	def __init__(self,attribute_generator_config,rng,agents_count):
		self.agents = []
		attribute_generator = agent_manager.load_attributes_generator(attribute_generator_config,rng)
		self.agents = agent_manager.generate_agents(attribute_generator,agents_count)