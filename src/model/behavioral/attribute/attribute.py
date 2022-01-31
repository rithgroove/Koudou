class Attribute:

	def __init__(self,name,value):
		self.name = name
		self.value = value

	def get_value(self):
		return self.value

	#interface for validating the value is within correct range
	#def validation(self):

	#interfact for generating the value randomly (correct range & distribution)
	#def generation(self):

	def update(self):
		return True