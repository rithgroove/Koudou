import csv
from .attribute.generator_attribute import GeneratorAttribute
from src.util.csv_reader import read_csv_as_dict
from src.model.behavioral.activity.condition import Condition
from src.model.behavioral.activity.condition_random import ConditionRandom
from src.model.behavioral.activity.activity import Activity
from .agent import Agent
from .behavior import Behavior
#from src.model.behavioral.activity.reward import Reward
def load_attributes_generator(file_names,rng):
	return GeneratorAttribute(file_names,rng)

def load_conditions(condition_files,rng):
	conditions = {}
	for condition_file in condition_files:
		data = read_csv_as_dict(condition_file)
		for x in data:
			if x["target"] == "random":
				conditions[x["name"]] = ConditionRandom(x["name"],x["value"],x["min"],x["max"],rng,x["operator"],x["type"],x["target"])
			else:
				conditions[x["name"]] = Condition(x["name"],x["attribute"],x["value"],x["operator"],x["type"],x["target"])
	return conditions
	
def generate_agents(kd_map,attribute_generator,n_agents):
	agents = []
	for ag_id in range(n_agents):
		agent = Agent(ag_id)
		attribute_generator.generate_attribute(agent, kd_map)
		agents.append(agent)
	attribute_generator.generate_household_attribute(agents,kd_map)
	return agents

def load_activities(activity_file,conditions_dict, rng):
	data = read_csv_as_dict(activity_file)
	activities = []
	for x in data:
		act = Activity(x["name"],x["conditions_type"])
		for y in x["conditions"].split(","):
			act.add_condition(conditions_dict[y])
		for y in x["actions"].split(","):
			act.add_action(y)
		activities.append(act)
	return activities

def load_behavior(name,file_name,condition_dict, rng):
	behavior = Behavior(name)
	activities = load_activities(file_name,condition_dict, rng)
	behavior.activities = activities
	return behavior
