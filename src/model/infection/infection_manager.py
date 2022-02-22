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
        d = Disease(d_config["name"], d_config["attributes"], d_config["transition_states"])
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

def step_infection(step_size: int, kd_map: Map, population: List[Agent], infection_module: Infection, rng):
    for ag in population:
        for disease in infection_module.diseases.values():
            current_state = ag.get_attribute(disease.name)
            next_state = current_state

            if current_state != "susceptible":
                rand_value = rng.random()
                previous_chances = 0
                for compartiment, attr in disease.transitions[current_state].items():
                    chance = apply_time_scale(step_size, attr["scale"], attr["probability"])
                    if rand_value < previous_chances + chance:
                        next_state = compartiment
                        break
                    previous_chances += chance
            else:
                call_complex_function()
            
            ag.set_attribute(disease.name, next_state)


def call_complex_function():
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




