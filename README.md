# Koudou
Modular small community simulator

This repository contains the simulator used for the paper: Mitsuteru Abe, Fabio Tanaka, Jair Pereira Junior, Anna Bogdanova, Tetsuya Sakurai, and Claus Aranha. 2022. **Using Agent-Based Simulator to Assess Interventions Against COVID-19 in a Small Community Generated from Map Data.** In Proceedings of the 21st International Conference on Autonomous Agents and Multiagent Systems (AAMAS '22). International Foundation for Autonomous Agents and Multiagent Systems, Richland, SC, 1–8.

## How to reproduce the results:
- Download the .osm file for the tsukuba area and place it on: osm_files/Tx-To-TU.osm
    - To download the file go to: https://www.openstreetmap.org/export and set the following coordinates:
        - minlat="36.0777000" 
        - minlon="140.0921000" 
        - maxlat="36.1217000"
        - maxlon="140.1201000"
    - Or download using the API req:
        https://www.openstreetmap.org/api/0.6/map?bbox=140.0921%2C36.0777%2C140.1201%2C36.1217
- change the configurations on 
- run: $ python main.py -p parameters/default.py

# Config file description (draft)

parameters/default:
	Defines general configugarition of the simulation and where are the files that describe how the agents/ionfection should behave
	- MAX_DAYS refer to the number of steps the simulation should run (I am changing the name of this var)

config/[Behavioral, evacuation, infection]
	These are the default actions/attributes agents will have in different scenarios

	Attributes:
		Describe attributes that agents/targets will have: Eg. Hunger, walking speed, energy, etc/
		- Basic: are attributes that start as a fixed value
		- Option: are categorical values from a list of possible values, usually are not numeric
		- Scheduled: attributes that just appear after some time has passed
		- Updatable: attributes that are updated every step
	Behavior:
		Describe what the actions agents should do when certain condition is met. The consequences of this actions can move the agent or change their attributes or behaviors
		- please note that the default result of an action is increase certain attribute, if you want to decrease, you have to write (minus)
	Condition:
		Describe attributes that a target will have if it meet certain conditions
	Profession:
		Describes which professions the agent may have and the work hours of them


	The infection config also has json that describes how the infection works:
		- Each type of infection has 2 files, the one that describes the transition probabilities and one that describes the probabilities of the disease spread

config/map
	These files describes the how the map should be built, if you want to simulate other cities, this files shiould be changed.

	Business.csv:
		Describe the open hours for businesses, places where people work,

	evacuation_center.json:
		Describe where in the map the evactuations should be. They could be described by the exact building_id, the building_type or which coordinate the evacuation center will be

	tsukuba-tu-building-data.csv
		Describes how many untagged buildings of each type should be in every coordinbate

	
