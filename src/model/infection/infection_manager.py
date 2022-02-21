import json
from typing import List

from infection import Infection
from src.model.behavioral.agent import Agent
from src.model.map.map import Map

from .disease import Disease

def initialize_infection(config):
    diseases = []
    for disease_file in config["disease"]:
        with open(disease_file) as file:
            d_config = json.load(file)
            d = Disease(d_config["name"], d_config["attributes"], d_config["transition_states"])
            diseases.append(d)

    return Infection()



def step_infection(kd_map: Map, agents: List[Agent], infection_module: Infection, rng):
    for ag in agents:
        for disease in infection_module.diseases.values():
            current_state = ag.get_attribute(disease.name)
            next_state = current_state

            if current_state != "susceptible":
                rand_value = rng.rand()
                previous_chances = 0
                for compartiment, attr in disease.transitions[current_state].items():
                    chance = apply_time_scale(attr["scale"], attr["probability"])
                    if rand_value < previous_chances + chance:
                        next_state = compartiment
                        break
                    previous_chances += chance
            else:
                call_complex_function()
            
            ag.set_attribute(disease.name, next_state)


def call_complex_function():
    pass

def apply_time_scale(time_scale, chance):
    if time_scale == "per_second":
        return chance
    elif time_scale == "per_minute":
        return chance/60
    elif time_scale == "per_hour":
        return chance/(60*60)
    elif time_scale == "per_day":
        return chance/(60*60*24)




