import src.util.csv_reader as csv_reader

class GeneratorAttribute:

	def __init__(self,attribute_files):
		self.attributes = []		
		self.load_basic_attribute(attribute_files["basic"])

		self.load_option_based_attribute(attribute_files["option"])
		

		#self.option = csv_reader.read_csv_as_dict(attribute_files["option"])
		
		self.updateable = csv_reader.read_csv_as_dict(attribute_files["updateable"])
		print(self)

	def generate_attribute(self,agent):
		#add attribute to the agent
		return agent

	def load_basic_attribute(self,file):
		basic_attributes  = csv_reader.read_csv_as_dict(file)
		self.basic = {}
		for attr in basic_attributes:
			self.basic[attr["name"]] = attr["value"]

	def load_option_based_attribute(self,file):
		option_based_attributes  = csv_reader.read_csv_as_dict(file)
		self.option = {}	
		for attr in option_based_attributes:
			print(attr)
			#self.option[attr["name"]] = attr["value"]


	def __str__(self):
		tempstring = "[Attribute Generator]\n"
		tempstring += f"Basic attributes = {len(self.basic)}\n"
		for x in self.basic:
			tempstring+= f"   -{x} : {self.basic[x]}\n"
		tempstring += f"Basic attributes = {len(self.basic)}\n"
		tempstring += f"Basic attributes = {len(self.basic)}\n"

		return tempstring