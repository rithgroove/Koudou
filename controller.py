import os
import osmium
from pathlib import Path
from os import path, mkdir
import threading
from src.model.behavioral.agent import Agent

from src.view.view import View
from src.model.map.map_manager import build_map
from src.logger import Logger

from src.view.draw import ViewPort
from src.model.behavioral.simulation import Simulation
import pickle
from platform import system
import numpy as np
class Controller():
    def __init__(self, parameters):
        self.d_param = parameters
        self.OS = self.d_param["OS"]

        self.logger = None
        self.view   = None
        self.map    = None
        self.sim    = None

        self.thread_finished = True
        self.rng = np.random.default_rng(seed = 101512)
        self.step_length = self.d_param["step_length"]

        # bindings
        if self.d_param["USE_VIEW"]:
            self.use_view()
        else:
            self.bind_no_view()

        if self.d_param["MAP_CACHE"] is not None and os.path.isfile(self.d_param["MAP_CACHE"]):
            self.load_map(self.d_param["MAP_CACHE"])
        else:
            self.load_map(self.d_param["MAP"])

        self.__load_sim(self.d_param)

        self.init_logger()

    def print_map(self):
        self.print_msg(self.map)

    ## open and close ##
    def main_loop(self):
        if self.d_param["USE_VIEW"]:
            self.step()
            if self.sim is not None:
                self.view.draw_agents(agents=self.sim.agents, viewport=self.viewport)
            self.view.main_loop()
            #need to call sim.step here

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
            view.canvas.bind("<Button>", self.on_mouse_scroll)

        self.mouse_prev_position = None

        # window
        view.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # buttons
        view.buttons["map_load"]["command"] = self.load_map
        view.buttons["sim_step"]["command"] = self.run_step
        view.buttons["rnd_ag"]["command"] = self.focus_random_agent
        view.zoom_in_btn["command"] = self.on_zoom_in
        view.zoom_out_btn["command"] = self.on_zoom_out

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
                                 grid_size    = self.d_param["GRID_SIZE"])

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
    def load_sim(self, config): pass
    def __load_sim(self, config):
        self.sim = Simulation(config["sim_config"],
                              self.map, self.rng, config["n_agents"], threads=1)




    def __load_map_view(self, osm_file=None):
        if osm_file is None:
            osm_file = self.view.ask_load_file()

        self.__load_map(osm_file)

        self.viewport = ViewPort(height=self.view.canvas.winfo_height(),
                                 width=self.view.canvas.winfo_width(),
                                 wmin=self.map.min_coord.get_lon_lat(),
                                 wmax=self.map.max_coord.get_lon_lat())

        self.view.draw_places(d_places=self.map.d_places, viewport=self.viewport)
        self.view.draw_roads (roads=self.map.main_road, d_nodes=self.map.d_nodes, viewport=self.viewport)

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
        self.viewport.update_scale(self.d_param["ZOOM_IN"])
        self.view.zoom(self.d_param["ZOOM_IN"])

    def on_zoom_out(self):
        self.viewport.update_scale(self.d_param["ZOOM_OUT"])
        self.view.zoom(self.d_param["ZOOM_OUT"])

    ## MOVING THE MAP ##
    def on_mouse_release(self, event):
        self.mouse_prev_position = None

    def on_mouse_hold(self, event):
        x, y  = event.x, event.y
        if self.mouse_prev_position is not None:
            px, py = self.mouse_prev_position
            self.viewport.update_center(px-x, py-y)

        self.mouse_prev_position = (x, y)
        self.view.canvas.scan_dragto(int(self.viewport.x), int(self.viewport.y), gain=1)

    def focus_random_agent(self):
        ag: Agent = self.rng.choice(self.sim.agents)
        x, y = self.viewport.apply(*ag.coordinate.get_lon_lat())

        new_x = -1*x + self.view.canvas.winfo_width()/2
        new_y = -1*y + self.view.canvas.winfo_height()/2

        self.viewport.change_center(new_x, new_y)
        self.view.canvas.scan_dragto(int(self.viewport.x), int(self.viewport.y), gain=1)


    ## LOGGER
    def init_logger(self):
        self.logger = Logger(exp_name=self.d_param["EXP_NAME"])

        # init all files
        files   = ["buildings.csv",
                   "agents.csv"]
        headers = [",".join(["id", "lon", "lat", "tags"]),
                   ",".join(["id", "lon", "lat"])]
        self.logger.add_files(files, headers)

    ## SIM
    def step(self):
        self.thread = threading.Thread(target=self.run_step, args=())
        self.thread.start()

    def run_step(self):
        self.thread_finished = False
        print("Processing... ", end="", flush=True)
        # self.model.step(stepSize=self.view.steps_to_advance)
        # self.update_view()

        # log data
        self.prepare_log()
        print("Done!", flush=True)
        self.thread_finished = True

    def prepare_log(self):
        # file 1
        clon = [self.map.d_places[id].render_info.center.lon for id in self.map.d_places.keys()]
        clat = [self.map.d_places[id].render_info.center.lat for id in self.map.d_places.keys()]
        tag1 = [",".join(self.map.d_places[id].render_info.tags) for id in self.map.d_places.keys()]
        data = [clon, clat, tag1]

        self.logger.write_data(filename="buildings.csv", data=data)

        # file 2
        attr1 = [None]
        attr2 = [None]
        attr3 = [None]
        data = [attr1, attr2, attr3]

        self.logger.write_data(filename="agents.csv", data=data)




if __name__ == "__main__":
    crtl = Controller()
    crtl.use_view()
    crtl.main_loop()
