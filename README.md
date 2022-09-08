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