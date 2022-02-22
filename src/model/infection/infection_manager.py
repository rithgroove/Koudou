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
            d_config["infectious_states"]
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


def disease_transmission(step_size: int, kd_map: Map, population: List[Agent], disease: Disease, rng):
    infected_agents = [ag for ag in population if ag.get_attribute(disease.name) in disease.infectious_states]
    for ag in infected_agents:
        n_id = ag.get_attribute("current_node_id")
        node = kd_map.d_nodes[n_id]
        print(node)
        pass
    pass

def apply_time_scale(step_size, time_scale, chance):
    if time_scale == "per_second":
        return chance*step_size
    elif time_scale == "per_minute":
        return chance*step_size/60
    elif time_scale == "per_hour":
        return chance*step_size/(60*60)
    elif time_scale == "per_day":
        return chance*step_size/(60*60*24)
