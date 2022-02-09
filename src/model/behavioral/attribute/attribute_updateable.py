from .attribute import Attribute

class AttributeUpdateable(Attribute):
	
	def __init__(self,name, value, min_val, max_val, step_reduction):
		super(AttributeUpdateable,self).__init__(name,value)
		self.min_val = min_val
		self.max_val = max_val
		self.step_reduction = step_reduction


	def set_max(self):
		self.value = self.max_val

	def set_min(self):
		self.value = self.min_val
