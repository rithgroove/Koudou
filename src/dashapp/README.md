# Simulator Dashboard V2
Deployment resource for Simulator Dashboard: [Dash Plotly](https://plotly.com/dash ) & [GitHub](https://github.com/plotly/dash ) <br>

**Updates in V2**
1. Data processing for a large quantity of result, integrate it between model and dashboard evaluation.
2. Multiple pages for <em>infection analytics</em>, <em>evacuation analytics</em>, <em>config query</em>, and <em>home page</em>.
3. Refactor codes: files, css, and modules for pages.
4. Clear instructions for file deployment.


## Deployment
``pip install plotly`` <br>
``pip install dash``<br>
``pip install jupyter -dash``
### File Deployment (Rough Version)
1. Directly modify markdown files content from `./dashapp/data/home/markdown_files/*`.
2. Move all csv files from `Koudou/results/test_config_file/*/*` to `./dashapp/data/test_result` directory.
3. Move all log files to `log_result`.
### Initiate Dashboard
Run App.py, and access on local with link:
http://127.0.0.1:8050/


## Data
### Used Files
<strong>Source1. Simulator running result</strong>
1. <strong>Home Page</strong> <br>
   This page mainly describe brief introduction about the simulator and the dashboard for demonstration.
   1. All images store in `./dashapp/data/Home/imgs`
   2. All markdown files store in `./dashapp/data/Home/markdown_files` 
2. <strong>Configuration Brief Page</strong> <br>
   Based on files from `Koudou/parameters/deafult.py` and `Koudaou/config/*`, the dashboard filters several important files 
   and configurations to display. Key configurations and initialized parameters about the simulator, and tuned parameters after simulation result comes out.
3. <strong>Infection Analytics</strong>
   From `Koudou/results/test_config_file/*/*`, results from simulation are calculated.
   1. `activity_history.csv`
   2. `disease_transition.csv`
   3. `infection_summary.csv`
   4. `new_infection.csv`
4. <strong>Evacuation Analytics</strong> <br>
   Same source directory: `Koudou/results/test_config_file/*/*`
   1. TBD
5. <strong>Not used yet</strong> <br>
   Same source directory: `Koudou/results/test_config_file/*/*`
   1. `agent_position_summary.csv`
   2. `evacuation.csv`
   3. `infection_transition.csv`

<strong>Source2. Log files from log module</strong> <br>
From the log module, more parameters will be generated during the simulation, which will be used for perfect the dashboard.
1. TBD


## TODO List
### Home Page
1. Draft description and abstract about the simulator and research.
2. Diagram suitable for demonstration.
### Configuration Page
1. Show all configuration files by category (behavioral, evacuation, infection, map)
2. List selective key parameters at the top of the page
   1. Number of agents
   2. To be Added...
### Simulator Result Page (From Log Module)
1. Present intermediate and final result of simulator (mainly from the log module)
   1. Start and end real time of the simulator (Simulation Duration comparing to duration inside the simulator world)
   2. Tuned parameters of simulators
   3. To be Added...
2. Present plain log from log files (waiting for categorizing)
### Infection Page
1. A filter to search a single agent health condition during the infection process
2. <strong>[DONE]</strong> List all related result files using filtering
3. <strong>[DONE]</strong> Infection line chart and pie chart
4. To be Added...
### Evacuation Page
1. A filter to search a single agent every movement during the evacuation
2. List all related result files using filtering
3. To be Added...
### Map Page (TODO?)
1. Brief description about the Map
   1. Range
   2. To be Added...
2. How to interpret?   
