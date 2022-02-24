import json
from typing import Dict, List
from src.model.behavioral.attribute.attribute import Attribute
from .infection import Infection
from src.model.behavioral.agent import Agent
from src.model.map.map import Map

from .disease import Disease


def initialize_infection(disease_files, population: List[Agent], rng):
    diseases = []

    for file_name in disease_files:
        with open(file_name) as file:
            d_config = json.load(file)
        
        d = Disease(
            d_config["name"],
            d_config["attributes"],
            d_config["transition_states"],
            d_config["infection_file"],
            d_config["infectious_states"],
            d_config["infected_starting_state"]
        )
        diseases.append(d)

        initializate_disease_on_population(d, d_config["initialization"], population, rng)

    return Infection(diseases)


def initializate_disease_on_population(disease: Disease, initialization: Dict, population: List[Agent], rng):
    for ag in population:
        new_attr = Attribute(disease.name, "susceptible")
        ag.add_attribute(new_attr)


    qtd = 0
    if initialization["type"] == "absolute":
        qtd = initialization["value"]
    elif initialization["type"] == "percentage":
        qtd = len(population) * initialization["value"]
    
    infected_ags = rng.choice(population, qtd, replace = False)
    for ag in infected_ags:
        ag.set_attribute(disease.name, initialization["state"])

def infection_step(step_size: int, kd_map: Map, population: List[Agent], infection_module: Infection, rng):
    # next state of the infected agents
    for disease in infection_module.diseases.values():
        infected_agents = [ag for ag in population if ag.get_attribute(disease.name) != "susceptible"]
        for ag in infected_agents:
            infected_next_stage(step_size, ag, disease, rng)

    # infection to healthy agents
    for disease in infection_module.diseases.values():
        disease_transmission(step_size, kd_map, population, disease, rng)

    

def infected_next_stage(step_size, ag: Agent, disease: Disease, rng):
    current_state = ag.get_attribute(disease.name)
    next_state = current_state

    if current_state in disease.transitions:
        rand_value = rng.random()
        previous_chances = 0
        for compartiment, attr in disease.transitions[current_state].items():
            chance = apply_time_scale(step_size, attr["scale"], attr["probability"])
            if rand_value < previous_chances + chance:
                next_state = compartiment
                break
            previous_chances += chance
    else:
        print(f"Could not find transition for state {current_state} of disease {disease.name}")

    ag.set_attribute(disease.name, next_state)

def apply_time_scale(step_size, time_scale, chance):
    if time_scale == "per_second":
        return chance*step_size
    elif time_scale == "per_minute":
        return chance*step_size/60
    elif time_scale == "per_hour":
        return chance*step_size/(60*60)
    elif time_scale == "per_day":
        return chance*step_size/(60*60*24)


def disease_transmission(step_size: int, kd_map: Map, population: List[Agent], disease: Disease, rng):
    infected_ags = [ag for ag in population if ag.get_attribute(disease.name) in disease.infectious_states]
    #ags_by_location = {ag.get_attribute("current_node_id"): [] for ag in population}
    ags_by_location = {}
    for ag in population:
        if ag.get_attribute("current_node_id") not in ags_by_location.keys():
            ags_by_location[ag.get_attribute("current_node_id")] = []
        ags_by_location[ag.get_attribute("current_node_id")].append(ag)
    for ag in infected_ags:
        loc = ag.get_attribute("current_node_id")
        if kd_map.is_businesses_node(loc):
            business_infection(step_size, ags_by_location[loc], disease, rng)
        elif kd_map.is_residences_node(loc):
            residence_infection(step_size, ag, ags_by_location[loc], disease, rng)
        elif kd_map.is_roads_node(loc):
            road_infection(step_size, kd_map, ag, ags_by_location, disease, rng)
        else:
            other_infection(step_size, ags_by_location[loc], disease, rng)

def business_infection(step_size, ag_same_location: List[Agent], disease, rng):
    infection_attr = disease.infection_method["businesses"]
    scale = infection_attr["scale"]
    prob = infection_attr["probability"]

    for ag in ag_same_location:
        if ag.get_attribute(disease.name) != "susceptible": #Already infected
            continue
        chance = apply_time_scale(step_size, scale, prob)
        if rng.uniform(0.0,1.0,1)[0] < chance: # infect agent
            ag.set_attribute(disease.name, disease.starting_state)


def residence_infection(step_size,infector:Agent, ag_same_location: List[Agent], disease, rng):
    infection_attr = disease.infection_method["residences"]
    scale = infection_attr["scale"]
    prob = infection_attr["probability"]

    for ag in ag_same_location:
        if ag.get_attribute(disease.name) != "susceptible":  # Already infected
            continue
        if ag.get_attribute("household_id") != infector.get_attribute("household_id"): #needs to be in the same household
            continue
        chance = apply_time_scale(step_size, scale, prob)
        if rng.uniform(0.0,1.0,1)[0] < chance:  # infect agent
            ag.set_attribute(disease.name, disease.starting_state)


def other_infection(step_size, ag_same_location: List[Agent], disease, rng):
    infection_attr = disease.infection_method["other"]
    scale = infection_attr["scale"]
    prob = infection_attr["probability"]

    for ag in ag_same_location:
        if ag.get_attribute(disease.name) != "susceptible":  # Already infected
            continue
        chance = apply_time_scale(step_size, scale, prob)
        if rng.uniform(0.0,1.0,1)[0] < chance:  # infect agent
            ag.set_attribute(disease.name, disease.starting_state)


def road_infection(step_size, kd_map: Map, infected_ag, ags_by_location, disease, rng):
    infection_attr = disease.infection_method["roads"]
    scale = infection_attr["scale"]
    gradient = infection_attr["gradient_by_distance"]
    cc_prob = infection_attr["close_contact_probability"] 

    loc = infected_ag.get_attribute("current_node_id")
    coor = infected_ag.coordinate
    susceptible_ags = ags_by_location[loc]
    for conn in kd_map.d_nodes[loc].connections:
        if (conn in ags_by_location.keys()):
            susceptible_ags += ags_by_location[conn]

    for ag in susceptible_ags:
        if ag.get_attribute(disease.name) != "susceptible":  # Already infected
            continue
        dist = ag.coordinate.calculate_distance(coor.lat,coor.lon)
        prob = cc_prob + gradient*dist
        chance = apply_time_scale(step_size, scale, prob)
        if rng.uniform(0.0,1.0,1)[0] < chance :  # infect agent
            ag.set_attribute(disease.name, disease.starting_state)
