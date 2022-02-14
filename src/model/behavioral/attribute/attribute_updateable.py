from .attribute import Attribute

class AttributeUpdateable(Attribute):
	
	def __init__(self,name, value, min_val, max_val, step_change):
		super(AttributeUpdateable,self).__init__(name,value)
		self.min_val = min_val
		self.max_val = max_val
		self.step_change = step_change

    def step(self,kd_sim,kd_map,ts,step_length,rng,agent):
    	self.value += self.step_change*step_length
    	self.value = max(self.value,self.min_val) #protect minimum cap
    	self.value = min(self.value, self.max_val) #protect max cap

	def set_max(self):
		self.value = self.max_val

	def set_min(self):
		self.value = self.min_val
