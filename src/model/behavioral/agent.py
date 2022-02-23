from src.model.map.coordinate import Coordinate
from src.model.behavioral.activity.action_move import ActionMove
class Agent:
	def __init__(self,agent_id):
		self.agent_id = agent_id
		self.attributes = {}
		self.default_behavior = None
		self.behaviors = {}
		self.actions = []
		self.active_action = None
		self.coordinate = Coordinate(0.0,0.0)

	def add_attribute(self,attr):
		self.attributes[attr.name] = attr

	def get_attribute(self,name):
		return self.attributes[name].get_value
	
	def update_attribute(self,attribute_name,value):
		print(f"value = {value}")
		if (value.lower() == "max"):
			self.attributes[attribute_name].set_max()
		elif(value.lower() == "min"):
			self.attributes[attribute_name].set_min()
		elif(self.attributes[attribute_name].typing == "string"):
			self.attributes[attribute_name].set_value(value)
		else:
			self.attributes[attribute_name].update_value(value)

	def set_attribute(self,attribute_name,value):
		self.attributes[attribute_name].set_value(value)

	def add_behavior(self,behavior):
		self.behaviors[behavior.name] = behavior

	def force_reset(self):
		if (isinstance(self.actions[0],ActionMove)):
			temp = self.actions[0]
			temp.force_reset()
			self.actions = [temp]
		else:
			self.actions = []

	def change_behavior(self,behavior_name):
		self.default_behavior = self.behaviors[behavior_name]

	def __str__(self):
		tempstring = "[Agent]\n"
		tempstring += f" Agent ID         = {self.agent_id}\n"
		tempstring += f" Current behavior = {self.default_behavior.name}\n"
		tempstring += f" Current location = (lat = {self.coordinate.lat}, lon {self.coordinate.lon})\n"
		tempstring += f" Current Actions  = {len(self.actions)}\n"
		tempstring += f" Attributes:\n"
		for x in self.attributes:
			tempstring +=  f"  - {x} = {self.attributes[x].get_value}\n"
		return tempstring

	def attribute_step(self,kd_sim,kd_map,ts,step_length,rng):
		#update attribute
		for attr in self.attributes:
			self.attributes[attr].step(kd_sim,kd_map,ts,step_length,rng,self)

	def behavior_step(self,kd_sim,kd_map,ts,step_length,rng):
		# if idle check action
		if len(self.actions) == 0:
			return self.default_behavior.step(kd_sim,kd_map,ts,step_length,rng,self) #get actions
		return []

	def action_step(self,kd_sim,kd_map,ts,step_length,rng):
		leftover = step_length
		while len(self.actions) > 0:
			act = self.actions[0]
			leftover = act.step(kd_sim,kd_map,ts,step_length,rng)
			if act.is_finished:
				self.actions.pop(0)
			else:
				break