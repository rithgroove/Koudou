from .attribute import Attribute

class AttributeOption(Attribute):
	def __init__(self,name, value,options):
		super(AttributeOption,self).__init__(name,value)
		self.options = options

	def get_options(self):
		return options
