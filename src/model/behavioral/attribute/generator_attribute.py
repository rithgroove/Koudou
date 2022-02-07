import src.util.csv_reader as csv_reader

from .attribute import Attribute
from .attribute_updateable import AttributeUpdateable
from .attribute_option import AttributeOption

class GeneratorAttribute:

	def __init__(self,attribute_files,rng):
		self.attributes = []		
		self.rng = rng
		self.basic = {}
		self.option = {}	
		self.updateable = {}
		self.profession = {}

		for filepath in attribute_files["basic"]:
			self.load_basic_attribute(filepath)

		for filepath in attribute_files["option"]:
			self.load_option_based_attribute(filepath)
		
		#self.option = csv_reader.read_csv_as_dict(attribute_files["option"])
		for filepath in attribute_files["updateable"]:
			self.load_updatable_attribute(filepath)

		for filepath in attribute_files["profession"]:
			self.load_profession(filepath)

	def load_basic_attribute(self,file):
		basic_attributes  = csv_reader.read_csv_as_dict(file)
		for attr in basic_attributes:
			self.basic[attr["name"]] = attr["value"]

	def load_option_based_attribute(self,file):
		option_based_attributes  = csv_reader.read_csv_as_dict(file)
		for attr in option_based_attributes:
			if (self.option.get(attr["name"]) is None):
				self.option[attr["name"]] = {}
				self.option[attr["name"]]["weights"] = []
				self.option[attr["name"]]["value"] = []
				self.option[attr["name"]]["options"] = []
			self.option[attr["name"]]["weights"].append(float(attr["weight"]))
			self.option[attr["name"]]["value"].append(attr["value"])
			option = {}
			option["value"]= attr["value"]
			option["weight"]= float(attr["weight"])
			self.option[attr["name"]]["options"].append(option)


	def load_updatable_attribute(self,file):
		updateable_attributes  = csv_reader.read_csv_as_dict(file)
		for attr in updateable_attributes:
			temp  = {}
			temp["name"] = attr["name"]
			temp["max"] = float(attr["max"])
			temp["min"] = float(attr["min"])
			temp["default_max"] = float(attr["default_max"])
			temp["default_min"] = float(attr["default_min"])
			temp["step_update"] = float(attr["step_update"])
			self.updateable[attr["name"]] = temp

	def load_profession(self,file):
		profession  = csv_reader.read_csv_as_dict(file)
		for attr in profession:
			print(attr)

	def generate_attribute(self,agent):
		#add attribute to the agent
		for attr in self.basic:
			agent.add_attribute(Attribute(x,self.basic[attr]))
		for key in self.updateable:
			attr = self.updateable[key]
			agent.add_attribute(AttributeUpdateable(key, self.rng.uniform(attr["default_min"],attr["default_max"],1)[0], attr["min"], attr["max"], attr["step_update"]))
		for key in self.option:
			value = np.random.choice(self.option[key]["value"],self.option[key]["weights"],1)
			print(value)
			agent.add_attribute(AttributeOption(key,value,self.option[key]["options"]))

		return agent


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
				tempstring+= f"     - {option['value']} : {option['weight']}\n"
		tempstring += f"\n"
		tempstring += f" Updateable attributes = {len(self.updateable)}\n"
		for key in self.updateable:
			tempstring+= f"   + {key} : \n"
			x = self.updateable[key]
			tempstring+= f"     - range            : {x['min']} - {x['max']} \n"
			tempstring+= f"     - initialization   : {x['default_min']} - {x['default_max']}\n"
			tempstring+= f"     - update (seconds) : {x['step_update']}\n"
			if (x.get("notes") is not None):
				tempstring+= f"     - notes            : {x['notes']}\n"
		return tempstring