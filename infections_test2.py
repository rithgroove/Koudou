import argparse
import numpy as np
from src.util.parser import load_parameters
from controller import Controller
from src.model.infection.infection_manager import initialize_infection, infection_step

def infection_decorator(ctrl: Controller, run_step_func, infection):
 
    # inner1 is a Wrapper function in
    # which the argument is called
     
    # inner function can access the outer local
    # functions like in this case "func"
    def inner1():
        run_step_func()
        infection_step(
            ctrl.d_param["STEP_LENGTH"], 
            ctrl.map, 
            ctrl.sim.agents, 
            infection, 
            ctrl.rng,
            ctrl.logger,
            ctrl.sim.ts
        )     
    return inner1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", dest='use_view', action='store_true', help="Use UI")
    parser.add_argument("-p", dest='param', help="Parameter File")
    args = parser.parse_args()

    parameters = load_parameters(args.param)
    parameters["USE_VIEW"] = args.use_view or parameters["USE_VIEW"]

    ctrl = Controller(parameters=parameters)
    
    rng = np.random.default_rng(seed=101512)
    infection = initialize_infection(parameters["DISEASES"], ctrl.sim.agents, rng, ctrl.logger)
    
    ctrl.run_step = infection_decorator(ctrl, ctrl.run_step, infection)

    ctrl.main_loop()

if __name__ == "__main__":
    main()