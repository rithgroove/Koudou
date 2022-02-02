class Agent:
	def __init__(self,agent_id):
		self.agent_id = agent_id
		self.attributes = {}

	def add_attribute(self,attr):
		self.attributes[attr.name] = attr

	def get_attribute(self,name):
		self.attributes[name].get_value
	
	def __str__(self):
		tempstring = "[Agent]\n"
		tempstring += f" Agent ID = {self.agent_id}\n"
		tempstring += f" Attributes:\n"
		for x in self.attributes:
			tempstring +=  f"  - {x} = {self.attributes[x].get_value}\n"
		return tempstring
