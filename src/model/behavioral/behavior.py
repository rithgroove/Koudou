from src.model.behavioral.activity.action_move import ActionMove

class Behavior:
	def __init__(self,name):
		self.name = name
		self.activities = []

	def add_activity(self,activity):
		self.activities.append(activity)

	def step(self,kd_sim,kd_map,ts,step_length,rng,agent,logger):
		move_action_pool = []
		for act in self.activities:
			if act.check_conditions(agent,kd_sim, kd_map, ts,rng):
				if agent.previous_activity != act.name:
					temp_activity = {
						"time_stamp": ts.step_count,
						"agent_id": agent.agent_id,
						"profession": agent.get_attribute("profession"),
						"location": agent.get_attribute("location"),
						"current_node_id": agent.get_attribute("current_node_id"),
						"household_id": agent.get_attribute("household_id"),
						"home_node_id": agent.get_attribute("home_node_id"),
						"activy_name": act.name,
					}
					logger.write_csv_data("activity_history.csv", temp_activity)
					agent.previous_activity = act.name
				actions = act.generate_actions(agent,kd_map,ts,rng)
				agent.actions.extend(actions)
				for action in actions:
					if action.__class__ is ActionMove:
						move_action_pool.append(action)
				break
		return move_action_pool


	def __str__(self):
		tempstring = "[Behavior]\n"
		tempstring += f"   Name = {self.name}"
		return tempstring