from src.model.behavioral.activity.action_move import ActionMove
from src.model.behavioral.activity.action_wait import ActionWait
from src.model.behavioral.activity.action_modify_attribute import ActionModifyAttribute

class Activity:
	def __init__(self,name):
		self.name = name
		self.condition = []
		self.rewards = []
		self.actions = []

	def add_condition(self,condition):
		self.condition.append(condition)

	def add_reward(self,reward):
		self.rewards.append(reward)

	def add_action(self,action):
		self.actions.append(action)

	def check_conditions(self,agent,kd_sim):
		result = True
		for x in self.condition:
			result = result and x.check_value(agent,kd_sim)
		return result

	def generate_actions(self,agent,kd_map,rng):
		actions = []
		for x in self.actions:
			temp = x.split(":")
			temp[0] = temp[0].replace(" ","")
			if (temp[0].lower() == "wait"):
				actions.append(ActionWait(agent,temp[1],rng))
			elif (temp[0].lower()=="move"):
				actions.append(ActionMove(agent,kd_map,temp[1],rng))
			elif (temp[0].lower()=="modify_attribute"):
				actions.append(ActionModifyAttribute(agent,temp[1]))
			elif (temp[0].lower()=="change_behavior"):
				actions.append(ActionModifyAttribute(agent,temp[1]))
		print(f"length = {len(actions)}")
		return actions

	def __str__(self):
		tempstring = "[Activity]\n"
		tempstring += f"   name = {self.name}\n"
		tempstring += f" Condition:\n"
		for x in self.condition:
			tempstring += f"   {x.short_string}\n"
		tempstring += f" Action:\n"
		for x in self.actions:
			tempstring += f"   {x.short_string}\n"
		tempstring += f" Reward:\n"
		for x in self.rewards:
			tempstring += f"   {x.short_string}\n"
		return tempstring