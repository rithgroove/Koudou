from src.model.map.coordinate import Coordinate

class Agent:
	def __init__(self,agent_id):
		self.agent_id = agent_id
		self.attributes = {}
		self.default_behavior = None
		self.actions = []
		self.active_action = None
		self.coordinate = Coordinate(0.0,0.0)

	def add_attribute(self,attr):
		self.attributes[attr.name] = attr

	def get_attribute(self,name):
		self.attributes[name].get_value
	
	def update_attribute(self,attribute_name,value):
		if (value == "max"):
			self.attributes.set_max()
		elif(value == "min"):
			self.attributes.set_min()
		elif("set" in value):
			self.attributes.set_value(value)
		else:
			self.attributes.update_value(value)

	def __str__(self):
		tempstring = "[Agent]\n"
		tempstring += f" Agent ID = {self.agent_id}\n"
		tempstring += f" Current location = (lat = {self.coordinate.lat}, lon {self.coordinate.lon})\n"
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
			return self.active_behavior.step(kd_sim,kd_map,ts,step_length,rng,self) #get actions
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