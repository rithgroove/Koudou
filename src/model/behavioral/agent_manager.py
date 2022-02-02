import csv
from .attribute.generator_attribute import GeneratorAttribute
from src.util.csv_reader import read_csv_as_dict
from src.model.behavioral.activity.condition import Condition
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

def test():
	print("test")