class Activity:
	def __init__(self,name):
		self.name = name
		self.condition = []

	def add_condition(self,condition):
		self.condition.append(condition)
