class ActionReward(Action):	
	def __init__(self,name,string):
        super(ActionMove,self).__init__(name)
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

	@property
	def short_string(self):
		return f"{self.attribute_name} = {self.value}\n"

	def __str__(self):
		tempstring = "[Reward]\n"
		tempstring += f"{self.attribute_name} = {self.value}"
		return tempstring