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
			if (self.option.get(attr["name"]) is None):
				self.option[attr["name"]] = {}
				self.option[attr["name"]]["options"] = []
				#self.option[attr["name"]]["default"] = None
			if (attr["default"].lower() == "true"):
				self.option[attr["name"]]["default"] = attr["value"]
			option = {}
			option["rand"] = float(attr["rand"])
			option["value"] = attr["value"]
			self.option[attr["name"]]["options"].append(option)

	def load_updatable_attribute(self,file):
		updateable_attributes  = csv_reader.read_csv_as_dict(file)
		self.updateable = {}
		for attr in updateable_attributes:
			self.updateable[attr["name"]] = attr
			attr["name"] = None
			attr["max"] = float(attr["max"])
			attr["min"] = float(attr["min"])
			attr["default_max"] = float(attr["default_max"])
			attr["default_min"] = float(attr["default_min"])
			attr["step_update"] = float(attr["step_update"])

	def __str__(self):
		tempstring = "[Attribute Generator]\n\n"
		tempstring += f" Basic attributes = {len(self.basic)}\n"
		for x in self.basic:
			tempstring+= f"   + {x} : {self.basic[x]}\n"
		tempstring += f"\n"
		tempstring += f" Option based attributes = {len(self.option)}\n"
		for x in self.option:
			tempstring+= f"   + {x} :\n"
			if self.option[x].get("default") is not None:
				tempstring+= f"     - Default Value = {self.option[x]['default']}\n"
			for option in self.option[x]["options"]:
				tempstring+= f"     - {option['value']} : {option['rand']}\n"
		tempstring += f"\n"
		tempstring += f" Updateable attributes = {len(self.updateable)}\n"
		for x in self.updateable:
			tempstring+= f"   + {x['name']} : \n"
			tempstring+= f"     - range            : {x['min']} - {x['max']} \n"
			tempstring+= f"     - initialization   : {x['default_min']} - {x['default_max']}\n"
			tempstring+= f"     - update (seconds) : {x['step_update']}\n"
			if (x.get("notes") is not None):
				tempstring+= f"     - notes            : {x['notes']}\n"
		return tempstring