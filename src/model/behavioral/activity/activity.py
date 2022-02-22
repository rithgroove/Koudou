from src.model.behavioral.activity.action_move import ActionMove
from src.model.behavioral.activity.action_wait import ActionWait
from src.model.behavioral.activity.action_modify_attribute import ActionModifyAttribute
from src.model.behavioral.activity.action_change_behavior import ActionChangeBehavior

class Activity:
	def __init__(self,name, command = "and"):
		self.name = name
		self.condition = []
		self.rewards = []
		self.actions = []
		self.command = command.lower()

	def add_condition(self,condition):
		self.condition.append(condition)

	def add_reward(self,reward):
		self.rewards.append(reward)

	def add_action(self,action):
		self.actions.append(action)

	def check_conditions(self,agent,kd_sim):
		result = True
		for x in self.condition:
			if (self.command.lower() == "and" or self.command.lower() == "none" ):
				result = result and x.check_value(agent,kd_sim)
				if not result:
					break
			elif (self.command.lower() == "or"):
				result = result or x.check_value(agent,kd_sim)
				if result:
					break
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
				actions.append(ActionChangeBehavior(agent,temp[1]))
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