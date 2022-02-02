class Activity:
	def __init__(self,name):
		self.name = name
		self.condition = []

	def add_condition(self,condition):
		self.condition.append(condition)

	def __str__(self):
		tempstring = "[Activity]\n"
		tempstring += f"   name = {self.name}\n"
		tempstring += f" Condition:\n"
		for x in self.condition:
			tempstring += f"   {x.math_string}\n"
		return tempstring