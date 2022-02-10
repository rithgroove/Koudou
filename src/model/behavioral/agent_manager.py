import csv
from .attribute.generator_attribute import GeneratorAttribute
from src.util.csv_reader import read_csv_as_dict
from src.model.behavioral.activity.condition import Condition
from src.model.behavioral.activity.activity import Activity
from .agent import Agent
from .behavior import Behavior
#from src.model.behavioral.activity.reward import Reward
def load_attributes_generator(file_names,rng):
	return GeneratorAttribute(file_names,rng)

def load_conditions(condition_file):
	data = read_csv_as_dict(condition_file)
	conditions = {}
	for x in data:
		if x["value"] == "$random":
			conditions[x["name"]] = Condition(x["name"],x["attribute"],x["value"],x["operator"])
		else:
			conditions[x["name"]] = Condition(x["name"],x["attribute"],x["value"],x["operator"])
	return conditions
	
def generate_agents(attribute_generator,count):
	agents = []
	for x in range(0,count):
		agent = Agent(x)
		attribute_generator.generate_attribute(agent)
		agents.append(agent)
	return agents

def load_activities(activity_file,conditions_dict, rng):
	data = read_csv_as_dict(activity_file)
	activities = []
	for x in data:
		act = Activity(x["name"])
		for y in x["conditions"].split(","):
			act.add_condition(conditions_dict[y])
		for y in x["actions"].split(","):
			temp = y.split(":")
			act.activities = temp
		activities.append(act)
	return activities

def load_behavior(name,file_name,condition_dict, rng):
	behavior = Behavior(name)
	activities = load_activities(file_name,condition_dict, rng)
	behavior.activities = activities
	return behavior

def test():
	print("test")
