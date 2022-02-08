import src.util.csv_reader as csv_reader
import numpy as np
from .attribute import Attribute
from .attribute_updateable import AttributeUpdateable
from .attribute_option import AttributeOption
from .attribute_grouped_schedule import AttributeGroupedSchedule
from .attribute_schedule import AttributeSchedule

class GeneratorAttribute:

	def __init__(self,attribute_files,rng):
		self.attributes = []		
		self.rng = rng
		self.basic = {}
		self.option = {}	
		self.updateable = {}
		self.professions = []
		self.counter = 0
		self.max_weight = 0
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
		professions  = csv_reader.read_csv_as_dict(file)
		for attr in professions:
			profession = {}
			profession["name"] = attr["name"]
			profession["place"] = attr["place"]
			profession["min_workhour"] = int(attr["min_workhour"])
			profession["max_workhour"] = int(attr["max_workhour"])
			profession["min_workday"] = int(attr["min_workday"])
			profession["max_workday"] = int(attr["max_workday"])
			profession["min_start_hour"] = int(attr["min_start_hour"])
			profession["max_start_hour"] = int(attr["max_start_hour"])
			profession["weight"] = int(attr["weight"])
			self.max_weight += profession["weight"]
			profession["off_map"] = attr["off_map"]
			profession["schedule"] = []
			if attr["schedule"] == "weekday": 
				profession["schedule"] = ["Mon","Tue","Wed","Thu","Fri"]
			elif attr["schedule"] == "weekend": 
				profession["schedule"] = ["Sat","Sun"]
			elif attr["schedule"] == "everyday": 
				profession["schedule"] = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
			else: 
				profession["schedule"] = attr["schedule"].split(",")
			profession["schedule"]= np.array(profession["schedule"])
			self.professions.append(profession)

	def generate_attribute(self,agent):
		#add attribute to the agent
		for attr in self.basic:
			agent.add_attribute(Attribute(attr,self.basic[attr]))
		for key in self.updateable:
			attr = self.updateable[key]
			agent.add_attribute(AttributeUpdateable(key, self.rng.uniform(attr["default_min"],attr["default_max"],1)[0], attr["min"], attr["max"], attr["step_update"]))
		for key in self.option:
			value = self.rng.choice(self.option[key]["value"],1,p=self.option[key]["weights"])[0]
			agent.add_attribute(AttributeOption(key,value,self.option[key]["options"]))
		#agent profession

		counter = self.counter % self.max_weight
		temp = None
		for prof in self.professions:
			if prof["weight"] > counter:
				temp = prof
				break
			else:
				counter -= prof["weight"]
		self.counter+=1
		start_time = self.rng.integers(temp["min_start_hour"],temp["max_start_hour"]+1,1)[0]
		workhour = self.rng.integers(temp["min_workhour"],temp["max_workhour"]+1,1)[0]
		end_time = (start_time + workhour)%24
		workday = self.rng.integers(temp["min_workday"],temp["max_workday"]+1,1)[0]

		### randomize day

		workdays = temp["schedule"]
		self.rng.shuffle(workdays,axis = 0)
		workdays = workdays[:workday]
		
		###---just for sorting from mon to sun--
		temp2 = []
		for x in ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]:
			if x in workdays:
				temp2.append(x)
		workdays =temp2
		
		###---sorting done---

		agent.add_attribute(Attribute("profession",temp["name"]))
		agent.add_attribute(Attribute("workplace_type",temp["place"]))
		agent.add_attribute(Attribute("start_time",start_time))
		agent.add_attribute(Attribute("end_time",end_time))
		agent.add_attribute(Attribute("workhour",workhour))
		agent.add_attribute(Attribute("workday",workday))
		agent.add_attribute(Attribute("schedule", ",".join(workdays)))
		agent.add_attribute(Attribute("off_map", temp["off_map"]))
		profession = AttributeGroupedSchedule("is_working_hour")

		for x in workdays:
			profession.add_schedule(AttributeSchedule(f"work-{x}", start_time*3600,end_time*3600, day_str = x,repeat = True))
		agent.add_attribute(profession)


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
		tempstring += f"\n"
		tempstring += f" Professions = {len(self.professions)}\n"
		for profession in self.professions:
			tempstring += f"   + {profession['name']} :\n"
			tempstring += f"     - place         : {profession['place']}\n"
			tempstring += f"     - working days  : {profession['min_workday']} - {profession['max_workday']} days\n"
			tempstring += f"     - duration      : {profession['min_workhour']} - {profession['max_workhour']} hours\n"
			tempstring += f"     - starting hour : {profession['min_start_hour']} - {profession['max_start_hour']} o'clock\n"
			tempstring += f"     - weight        : {profession['weight']}\n"
			if profession["off_map"].lower() == "true":
				tempstring += f"     - off_map        : True\n"
			else:
				tempstring += f"     - off_map        : False\n"
			tempstring += f"     - schedule      : {','.join(profession['schedule'])}\n"
		return tempstring