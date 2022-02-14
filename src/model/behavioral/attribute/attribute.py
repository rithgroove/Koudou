class Attribute:

	def __init__(self,name,value):
		self.name = name
		self.value = value

	@property
	def get_value(self):
		return self.value

	def set_value(self,value):
		self.value = value

	def update_value(self,value):
		self.value+=value

	def set_max(self):
		pass

	def set_min(self):
		pass
		
	#interface for validating the value is within correct range
	#def validation(self):

	#interfact for generating the value randomly (correct range & distribution)
	#def generation(self):

	def update(self,kd_sim,kd_map,ts,step_length):
		pass