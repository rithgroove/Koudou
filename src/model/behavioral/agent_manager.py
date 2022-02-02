import csv
from .attribute.generator_attribute import GeneratorAttribute
from src.util.csv_reader import read_csv_as_dict
from src.model.behavioral.activity.condition import Condition
from src.model.behavioral.activity.activity import Activity
def load_attributes_generator(file_names,rng):
	return GeneratorAttribute(file_names,rng)

def load_condition(condition_file,rng):
	data = read_csv_as_dict(condition_file)
	conditions = {}
	for x in data:
		if x["value"] == "$random":
			conditions[x["name"]] = Condition(x["name"],x["attribute"],x["value"],x["operator"])
		else:
			conditions[x["name"]] = Condition(x["name"],x["attribute"],x["value"],x["operator"])
	return conditions

def load_activities(activity_file,conditions_dict, rng):
	data = read_csv_as_dict(activity_file)
	activities = []
	for x in data:
		act = Activity(x["name"])
		for y in x["conditions"].split(","):
			act.add_condition(conditions_dict[y])
		activities.append(act)
	return activities

def test():
	print("test")

