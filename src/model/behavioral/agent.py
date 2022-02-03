class Agent:
	def __init__(self,agent_id):
		self.agent_id = agent_id
		self.attributes = {}

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
		tempstring += f" Attributes:\n"
		for x in self.attributes:
			tempstring +=  f"  - {x} = {self.attributes[x].get_value}\n"
		return tempstring
