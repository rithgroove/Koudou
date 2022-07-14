import pickle
import threading
import numpy as np

from pathlib import Path
from os import path, mkdir#join, exists

from src.view.view import View
from src.view.draw import ViewPort

from src.logger import Logger

from src.model.map.map_manager import build_map

from src.model.behavioral.simulation import Simulation
from src.model.infection.infection_module import InfectionModule
from src.model.evacuation.evacuation_module import EvacuationModule

class Controller():
    def __init__(self, parameters):
        self.d_param = parameters
        self.OS = self.d_param["OS"]

        self.logger = None
        self.view   = None
        self.map    = None
        self.sim    = None

        self.thread_finished = True
        self.rng = np.random.default_rng(seed=self.d_param["SEED"])
        # self.step_length = self.d_param["STEP_LENGTH"]

        # bindings
        if self.d_param["USE_VIEW"]:
            self.use_view()
        else:
            self.bind_no_view()

        map = self.d_param["MAP_CACHE"] if self.d_param["MAP_CACHE"] else self.d_param["MAP"]
        if map is not None:
            self.load_map(map)

        if self.d_param["SIM_CONFIG"]:
            self.load_sim()

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

    ## binding ##
    def bind_no_view(self):
        self.load_map  = self.__load_map
        self.print_msg = self.__print_msg_noview
    def bind_with_view(self):
        self.load_map = self.__load_map_view
        self.print_msg = self.__print_msg_view

    ## view enable ##
    def use_view(self):
        self.view = View()
        self.bind_with_view()
        self.set_view_events()
    def set_view_events(self):
        # shortcuts
        view = self.view

        # scroll
        self.on_mouse_scroll = self.__scroll_mouse_wheel
        if self.OS == "Linux":
            self.on_mouse_scroll = self.__scroll_linux

        self.mouse_prev_position = None

        # window
        view.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # buttons
        view.buttons["map_load"]["command"] = self.load_map
        view.buttons["sim_step"]["command"] = self.run_step

        # canvas
        view.canvas.bind("<MouseWheel>"     , self.on_mouse_scroll)
        view.canvas.bind("<B1-Motion>"      , self.on_mouse_hold)
        view.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)


    ## print messages
    def print_msg(self):    pass
    def __print_msg_noview(self, msg):
        print(msg)
    def __print_msg_view(self, msg):
        self.view.update_log(msg)

    ## load map
    def load_map(self): pass
    def __load_map(self, osm_file=None):
        if osm_file is None:
            raise Exception(f"Map file not specified!")

        filename = Path(osm_file).stem
        fileext  = Path(osm_file).suffix

        if fileext==".osm":
            self.print_msg(f"Loading map: {filename}{fileext}")
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

    def __load_map_view(self, osm_file=None):
        if osm_file is None:
            osm_file = self.view.ask_load_file()

        self.__load_map(osm_file)

        self.ViewPort = ViewPort(height=self.view.canvas.winfo_height(),
                                 width=self.view.canvas.winfo_width(),
                                 wmin=self.map.min_coord.get_lon_lat(),
                                 wmax=self.map.max_coord.get_lon_lat())

        self.view.draw_places(d_places=self.map.d_places, viewport=self.ViewPort)
        self.view.draw_roads (roads=self.map.main_road, d_nodes=self.map.d_nodes, viewport=self.ViewPort)

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

    def on_zoom_in(self):
        self.ViewPort.update_scale(self.d_param["ZOOM_IN"])
        self.view.zoom(self.d_param["ZOOM_IN"])

    def on_zoom_out(self):
        self.ViewPort.update_scale(self.d_param["ZOOM_OUT"])
        self.view.zoom(self.d_param["ZOOM_OUT"])

    ## MOVING THE MAP ##
    def on_mouse_release(self, event):
        self.mouse_prev_position = None

    def on_mouse_hold(self, event):
        x, y  = event.x, event.y
        if self.mouse_prev_position is not None:
            px, py = self.mouse_prev_position
            self.ViewPort.update_center(px-x, py-y)

        self.mouse_prev_position = (x, y)
        self.view.canvas.scan_dragto(self.ViewPort.x, self.ViewPort.y, gain=1)

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

    def run_step(self):
        self.thread_finished = False
        # print("Processing... ", end="", flush=True)

        # LOGGING
        # infection summary
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

        # STEP
        self.sim.step(step_length = self.d_param["STEP_LENGTH"],
                      logger      = self.logger)

        # self.update_view()

        # print("Done!", flush=True)
        self.thread_finished = True

    def run_simulation(self):
        self.print_msg(f"Running simulation... 0/{self.d_param['MAX_DAYS']} days")
        for d in range(0, self.d_param["MAX_DAYS"]):
            self.run_step()

        self.print_msg(f"{d+1}/{self.d_param['MAX_DAYS']} days done")
        self.print_msg("")


if __name__ == "__main__":
    crtl = Controller()
    crtl.use_view()
    crtl.main_loop()
