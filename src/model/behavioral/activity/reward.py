class reward:
	def __init__(self,string):
		temp = string.split(":")		
		self.attribute_name = temp[0]
		if (temp[1].lower() == "max"):
			self.value = "max"
		elif(temp[1].lower() == "min"):
			self.value = "min"
		elif("set" in temp[1].lower):
			self.value = temp[1]
		else:
			self.value = float(temp[1])

	def apply_reward(self,agent):
		agent.update_attribute(self.attribute_name,self.value)