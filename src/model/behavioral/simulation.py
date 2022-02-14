from src.model.behavioral import agent_manager
from src.util.time_stamp import TimeStamp
import src.model.map.a_star as a_star
class Simulation:
	def __init__(self,config,rng,agents_count,threads = 1, cache_file_name = None, report = None):
		self.agents = []
		attribute_generator = agent_manager.load_attributes_generator(config["attribute_generator"],rng)
		self.agents = agent_manager.generate_agents(attribute_generator,agents_count)		
		self.conditions = agent_manager.load_conditions(config["condition"])
		self.behavior = agent_manager.load_behavior("normal", config["behavior"], self.conditions, rng)
		for x in self.agents:
			x.defaultBehavior = self.behavior
		self.rng = rng
		self.ts = TimeStamp(0)
		self.threads = threads
		self.cache_file_name = cache_file_name
		self.report = report

	def __str__(self):
		tempstring = "[Simulation]\n"
		tempstring += f"Total agents = {len(self.agents)}\n"
		tempstring += f"Condition = {len(self.conditions)}\n"
		return tempstring

	def test(self):
		for x in self.agents:
			print(x)

	def step(self,kd_map,step_length):
		ts.step(step_length)
		#update all agents attribute
		for agent in self.agents:
			agent.attribute_step(self,kd_map,self.ts,step_length,self.rng)

		#check for activities
		move_action_pool = []
		for agent in self.agents:
			move_actions = agent.behavior_step(self,kd_map,self.ts,step_length,self.rng)
			move_action_pool.extend(move_actions)

		self.pathfind(move_action_pool,kd_map)

		#need code to generate actions here
		for agent in self.agents:
			agent.attribute_step(self,kd_map,self.ts,step_length,self.rng)

	def pathfind(self,move_actions,kd_map):
		a_star.parallel_a_star(kd_map, start_goals_arr, n_threads=self.threads, cache_file_name = self.cache_file_name, report = self.report):



