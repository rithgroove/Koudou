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

	def check_conditions(self,agent):
		result = True
		for x in self.condition:
			result = result and x.check(agent)
		return result

	def generate_actions(self,agent,map,rng):
		actions = []
		for x in self.actions:
			temp = x.split(":")
			if (temp[0].lower() == "wait"):
				actions.append(ActionWait(temp[1]),agent,map,rng)
			elif (temp[0].lower()=="move"):
				actions.append(ActionMove(agent,map,temp[1]))
			elif (temp[0].lower()=="modify_attribute"):
				actions.append(ActionModifyAttribute(temp[1]))
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