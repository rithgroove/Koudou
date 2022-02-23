from src.model.behavioral import agent_manager
from src.util.time_stamp import TimeStamp
import src.model.map.a_star as a_star
class Simulation:
	def __init__(self,config,kd_map,rng,agents_count,threads = 1, cache_file_name = None, report = None):
		self.agents = []
		attribute_generator = agent_manager.load_attributes_generator(config["attributes"],rng)
		#print(attribute_generator)
		self.agents = agent_manager.generate_agents(kd_map,attribute_generator,agents_count)		
		self.conditions = agent_manager.load_conditions(config["condition"],rng)
		self.behaviors = {}
		for key in config["behaviors"]:
			self.behaviors[key] = agent_manager.load_behavior(key, config["behaviors"][key], self.conditions, rng)
		for x in self.agents:
			x.behaviors = self.behaviors
			x.default_behavior = self.behaviors[config["default_behavior"]]
		self.attributes = {}
		attribute_generator.generate_attribute_for_simulation(self,kd_map)
		self.rng = rng
		self.ts = TimeStamp(0)
		self.threads = threads
		self.kd_map = kd_map
		self.cache_file_name = cache_file_name
		self.report = report
		self.d_agents_by_location = {}
		self.modules = []

	def add_attribute(self,attr):
		self.attributes[attr.name] = attr

	def get_attribute(self,name):
		return self.attributes[name].get_value

	def __str__(self):
		tempstring = "[Simulation]\n"
		tempstring += f"Total agents = {len(self.agents)}\n"
		tempstring += f"Condition = {len(self.conditions)}\n"
		tempstring += f"Attributes:\n"
		for x in self.attributes:
			tempstring +=  f"  - {x} = {self.attributes[x].get_value}\n"

		return tempstring

	def test(self):
		for x in self.agents:
			print(x)

	def attribute_step(self,kd_sim,kd_map,ts,step_length,rng):
		#update attribute
		for attr in self.attributes:
			self.attributes[attr].step(kd_sim,kd_map,ts,step_length,rng,None)

	def step(self,step_length):
		self.ts.step(step_length)
		self.attribute_step(self,self.kd_map,self.ts,step_length,self.rng)
		##############################################################################
		# update all agents attribute
		##############################################################################
		for agent in self.agents:
			agent.attribute_step(self,self.kd_map,self.ts,step_length,self.rng)

		##############################################################################
		# check for activities
		##############################################################################
		move_action_pool = []
		for agent in self.agents:
			move_actions = agent.behavior_step(self,self.kd_map,self.ts,step_length,self.rng)
			move_action_pool.extend(move_actions)

		for x in move_action_pool:
			print(x)

		##############################################################################
		# pathfind
		##############################################################################
		if (len(move_action_pool) > 0):
			self.pathfind(move_action_pool)

		##############################################################################
		# action step
		##############################################################################
		for agent in self.agents:
			agent.action_step(self,self.kd_map,self.ts,step_length,self.rng)

		##############################################################################
		# construct location dictionary for ease of use
		##############################################################################
		self.group_agents_by_location()
		##############################################################################
		# evacuation
		##############################################################################
		for module in self.modules:
			module.step(self,self.kd_map,self.ts,step_length,self.rng)
		##############################################################################
		# epidemicon
		##############################################################################

	def group_agents_by_location(self):
		self.d_agents_by_location = {}
		for agent in self.agents:
			if (agent.get_attribute("current_node_id") not in self.d_agents_by_location.keys()):
				self.d_agents_by_location[agent.get_attribute('current_node_id')] = []
			self.d_agents_by_location[agent.get_attribute('current_node_id')].append(agent)

	def pathfind(self,move_actions):
		pool = []
		for x in move_actions:
			temp = (x.origin ,x.destination)
			if (temp not in pool):
				pool.append(temp)
		results = a_star.parallel_a_star(self.kd_map, pool, n_threads=self.threads, cache_file_name = self.cache_file_name, report = self.report)
		for x in move_actions:
			temp = (x.origin ,x.destination)
			x.generate_vector(self.kd_map, results[temp])

