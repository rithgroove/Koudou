#from .action import Action

# Do not use, under development

# class ActionGenerateAttribute(Action):	
# 	def __init__(self,command):
#         super(ActionModifyAttribute,self).__init__()
# 		temp = command.split(":")		
# 		self.attribute_name = temp[0]
# 		if (temp[1].lower() == "max"):
# 			self.value = "max"
# 		elif(temp[1].lower() == "min"):
# 			self.value = "min"
# 		elif("set" in temp[1].lower):
# 			self.value = temp[1]
# 		else:
# 			self.value = float(temp[1])
# 		self.is_finished = False

#     def update(self,step_length):
#         """
#         [Method]
#         Update method

#         parameter:
#         - step_length : (int) how many seconds elapsed

#         return:
#         - (int) the remainder of the step_length that was not consumed by this action
#         """
# 		agent.update_attribute(self.attribute_name,self.value)\
# 		self.is_finished = True
#         return step_length #return the left over time 

# 	@property
# 	def short_string(self):
# 		return f"{self.attribute_name} = {self.value}\n"

# 	def __str__(self):
# 		tempstring = "[Action_Modify_attribute]\n"
# 		tempstring += f"{self.attribute_name} = {self.value}"
# 		return tempstring


#     @property
#     def is_finished(self):
#         """
#         [Property]
#         Check if this action is finished or not

#         return:
#         - (bool) true if finished, false otherwise
#         """
#         return self.is_finished = False
