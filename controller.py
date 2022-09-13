import pickle
import threading
import numpy as np

from pathlib import Path
from os import path, mkdir
from src.model.map.map import Map#join, exists

from src.view.view import View
from src.view.viewport import ViewPort

from src.logger import Logger

from src.model.map.map_manager import build_map

from src.model.behavioral.simulation import Simulation
from src.model.infection.infection_module import InfectionModule
from src.model.evacuation.evacuation_module import EvacuationModule

from src.model.behavioral.agent import Agent

class Controller():
    def __init__(self, parameters):
        self.d_param = parameters
        self.OS = self.d_param["OS"]

        self.logger: Logger = None
        self.view: View   = None
        self.map: Map    = None
        self.sim: Simulation    = None

        self.thread_finished = True
        self.rng = np.random.default_rng(seed=self.d_param["SEED"])
        # self.step_length = self.d_param["STEP_LENGTH"]


        if self.d_param["MAP_CACHE"] is not None and path.isfile(self.d_param["MAP_CACHE"]):
            self.load_map(self.d_param["MAP_CACHE"])
        else:
            self.load_map(self.d_param["MAP"])

        if self.d_param["SIM_CONFIG"]:
            self.load_sim()

        # bindings
        if self.d_param["USE_VIEW"]:
            self.load_view()

        self.init_logger()

    def print_map(self):
        self.print_msg(self.map)

    ## open and close ##
    def main_loop(self):
        if self.d_param["USE_VIEW"]:
            # self.step()
            self.view.main_loop()

        else:
            self.run_simulation()
            self.on_closing()

    def on_closing(self):
        if self.d_param["USE_VIEW"]:
            self.view.close()

        self.logger.close_files()




    def set_view_events(self):
        # shortcuts
        view = self.view

        # scroll
        self.on_mouse_scroll = self.__scroll_mouse_wheel
        if self.OS == "Linux":
            self.on_mouse_scroll = self.__scroll_linux
            view.canvas.bind("<Button>", self.on_mouse_scroll)

        self.mouse_prev_position = None

        # window
        view.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # buttons
        view.buttons["map_load"]["command"] = self.load_map
        view.buttons["sim_step"]["command"] = self.run_step
        view.buttons["sim_run"]["command"]  = self.cmd_auto
        view.buttons["rnd_ag"]["command"] = self.focus_random_agent
        view.zoom_in_btn["command"] = self.on_zoom_in
        view.zoom_out_btn["command"] = self.on_zoom_out


        # canvas
        view.canvas.bind("<MouseWheel>"     , self.on_mouse_scroll)
        view.canvas.bind("<B1-Motion>"      , self.on_mouse_hold)
        view.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

  

    ## load map
    def load_map(self, osm_file=None):
        if osm_file is None and  self.d_param["USE_VIEW"]:
            osm_file = self.view.ask_load_file()
        elif osm_file is None:
            raise Exception(f"Map file not specified!")

        filename = Path(osm_file).stem
        fileext  = Path(osm_file).suffix

        if fileext==".osm":
            self.print_msg(f"Loading map: {filename}{fileext}")
            # todo: evac center should be in a module
            self.map = build_map(osm_file,
                                 bldg_tags    = self.d_param["BUILDING_TAGS"],
                                 business_data= self.d_param["BUSINESS"],
                                 grid_size    = self.d_param["GRID_SIZE"],
                                 evacuation_center = self.d_param["EVAC_CENTER"])

            ## temp pickling it here since loading takes time
            if not path.exists("cache"):
                mkdir("cache")

            with open(path.join("cache",f"{filename}.pkl"), "wb") as file:
                pickle.dump(self.map, file)
        elif fileext==".pkl":
            self.print_msg(f"Loading cached map: {filename}{fileext}")
            with open(osm_file, "rb") as file:
                self.map = pickle.load(file)
        else:
            self.print_msg(f"Not a valid map file")
            return

    def load_view(self):
        self.view = View()
        self.view_port = ViewPort(height=self.view.canvas.winfo_height(),
                                 width=self.view.canvas.winfo_width(),
                                 wmin=self.map.min_coord.get_lon_lat(),
                                 wmax=self.map.max_coord.get_lon_lat())

        self.view.draw.draw_places(d_places=self.map.d_places, viewport=self.view_port)
        self.view.draw.draw_roads(roads=self.map.main_road, d_nodes=self.map.d_nodes, viewport=self.view_port)
        self.view.draw.draw_agents(agent_list=self.sim.agents, viewport=self.view_port)
        self.view.clock.configure(text=self.sim.ts.get_hour_min_str())
        self.set_view_events()

    ## load sim
    def load_sim(self):
        self.sim = Simulation(config       = self.d_param["SIM_CONFIG"],
                              kd_map       = self.map,
                              rng          = self.rng,
                              agents_count = self.d_param["N_AGENTS"],
                              threads      = self.d_param["THREADS"],
                              report       = None
        )

        if self.d_param["DISEASES"]:
            # todo: we shouldnt pass thw whole simulator, just the necessary things
            # i guess just agents, but Im not changing this to avoid bugs
            self.sim.modules.append(
                InfectionModule(parameters = self.d_param["DISEASES"],
                                kd_sim     = self.sim,
                                rng        = self.rng))

        if self.d_param["EVACUATION"]:
            self.sim.modules.append(
                EvacuationModule(distance = self.d_param["EVACUATION"]["DISTANCE"],
                                 share_information_chance = self.d_param["EVACUATION"]["SHARE_INFO_CHANCE"]))


    ## ZOOM ##
    def on_mouse_scroll(self, event):   pass

    def __scroll_linux(self, event):
        if event.num == 4:
            self.on_zoom_in()
        elif event.num == 5:
            self.on_zoom_out()

    def __scroll_mouse_wheel(self, event):
        if event.delta < 0:
            self.on_zoom_in()
        elif event.delta > 0:
            self.on_zoom_out()

    def focus_random_agent(self):
        ag: Agent = self.rng.choice(self.sim.agents)
        x, y = self.view_port.apply(*ag.coordinate.get_lon_lat())

        new_x = int(-1*x + self.view.canvas.winfo_width()/2)
        new_y = int(-1*y + self.view.canvas.winfo_height()/2)

        self.view_port.change_center(new_x, new_y)
        self.view.canvas.scan_dragto(self.view_port.x, self.view_port.y, gain=1)

        self.print_msg("Agent info:")
        self.print_msg(ag.__dict__, "\n")

    def on_zoom_in(self):
        self.view_port.update_scale(self.d_param["ZOOM_IN"])
        self.view.zoom(self.d_param["ZOOM_IN"])

    def on_zoom_out(self):
        self.view_port.update_scale(self.d_param["ZOOM_OUT"])
        self.view.zoom(self.d_param["ZOOM_OUT"])

    ## MOVING THE MAP ##
    def on_mouse_release(self, event):
        self.mouse_prev_position = None

    def on_mouse_hold(self, event):
        x, y  = event.x, event.y
        if self.mouse_prev_position is not None:
            px, py = self.mouse_prev_position
            self.view_port.update_center(px-x, py-y)
            self.view.coord_label.configure(text=f"{px-x}, {py-y}")

        self.mouse_prev_position = (x, y)
        self.view.canvas.scan_dragto(self.view_port.x, self.view_port.y, gain=1)

    ## LOGGER
    def init_logger(self):
        self.logger = Logger(exp_name=self.d_param["EXP_NAME"])

        # health
        header = ["time_stamp","susceptible","exposed",
                  "asymptomatic","symptomatic","severe","recovered"]
        self.logger.add_csv_file("infection_summary.csv", header)

        # position
        header = ["time_stamp","location","count"]
        self.logger.add_csv_file("agent_position_summary.csv", header)

        # activity
        header = ["time_stamp","agent_id","profession","location",
                  "current_node_id","household_id","home_node_id","activy_name"]
        self.logger.add_csv_file("activity_history.csv", header)

        # new infections
        header = ["time_stamp","type","disease_name","agent_id",
                  "agent_profession","agent_location","agent_node_id",
                  "source_id","source_profession","source_location","source_node_id"]
        self.logger.add_csv_file("new_infection.csv", header)

        # infection transition
        header = ["time_stamp","disease_name","agent_id","agent_profession",
                  "agent_location","agent_node_id","current_state","next_state"]
        self.logger.add_csv_file("disease_transition.csv", header)

        # evacuation
        header = ["time_stamp","evacuated","unevacuated_ERI","unevacuated_no_ERI"]
        self.logger.add_csv_file("evacuation.csv", header)

        # time stamp?
        header = ["time_stamp","","",""]
        self.logger.add_csv_file("infection_transition.csv", header)

    ## SIM
    def step(self):
        self.thread = threading.Thread(target=self.run_step, args=())
        self.thread.start()

    def print_msg(self, msg):
        print(msg)

    def run_step(self):
        self.thread_finished = False
        # print("Processing... ", end="", flush=True)

        # LOGGING
        # infection summary
        ########################### LOGGING ###########################################
        temp = self.sim.summarized_attribute("covid")
        temp2 = {}
        temp2["time_stamp"] = self.sim.ts.step_count
        health_header = ["time_stamp","susceptible","exposed",
                  "asymptomatic","symptomatic","severe","recovered"]
        for x in health_header:
            if x in temp.keys():
                temp2[x] = temp[x]
            else:
                temp2[x] = 0

        self.logger.write_csv_data("infection_summary.csv", temp2)

        # agent position
        temp = self.sim.summarized_attribute("location")
        for x in temp.keys():
            temp2 = {}
            temp2["time_stamp"] = self.sim.ts.step_count
            temp2["location"]   = x
            temp2["count"]      = temp[x]

        self.logger.write_csv_data("agent_position_summary.csv", temp2)


        ###########################################################################
        # STEP
        self.sim.step(step_length = self.d_param["STEP_LENGTH"],
                      logger      = self.logger)

        # self.update_view() #todo: create an update loop, where we add move methods
        if self.d_param["USE_VIEW"]:
            self.view.draw.move_agents(agent_list=self.sim.agents, viewport=self.view_port)
            self.view.clock.configure(text=self.sim.ts.get_hour_min_str())

        # print("Done!", flush=True)
        self.thread_finished = True


    def run_simulation(self):
        self.print_msg(f"Running simulation... 0/{self.d_param['MAX_DAYS']} days")
        for d in range(0, self.d_param["MAX_DAYS"]):
            self.run_step()

        self.print_msg(f"{d+1}/{self.d_param['MAX_DAYS']} days done")
        self.print_msg("")

    def run_auto(self):
        self.thread_finished = False
        while not self.thread_ask_stop:
            self.run_step()
        self.thread_finished = True

    def cmd_auto(self):
        self.view.btn_start_change_method(text="Pause", method=self.cmd_pause)
        self.thread = threading.Thread(target=self.run_auto, args=())
        self.thread_ask_stop = False
        self.thread.start()

    def cmd_pause(self):
        self.view.btn_start_change_method(text="Play ", method=self.cmd_auto)
        self.thread_ask_stop = True


if __name__ == "__main__":
    crtl = Controller()
    crtl.use_view()
    crtl.main_loop()
