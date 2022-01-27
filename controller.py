import osmium
from pathlib import Path
from os import path, mkdir#join, exists

from src.view.view import View
from src.model.map.map_manager import build_map

from src.view.draw import ViewPort

import pickle
from platform import system

class Controller():
    def __init__(self):
        # view
        self.view = None
        self.map = None

        # bindings
        self.bind_no_view()


        self.OS = system()
        # scroll
        self.on_mouse_scroll = self.__scroll_mouse_wheel
        if self.OS == "Linux":
            self.on_mouse_scroll = self.__scroll_linux

        # parameters related to the view
        self.zoom_in_param  = 1.1
        self.zoom_out_param = (10.0/11.0)
        self.mouse_prev_position = None

    def print_map(self):
        self.print_msg(self.map)

    ## open and close ##
    def main_loop(self):
        self.view.main_loop()
    def on_closing(self):
        self.view.close()

    ## binding ##
    def bind_no_view(self):
        self.load_map  = self.__load_map_noview
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

        # window
        view.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # buttons
        view.buttons["map_load"]["command"] = self.load_map

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
    def __load_map_noview(self, osm_file):
        self.print_msg(f"Loading map: {Path(osm_file).stem}")
        self.map = build_map(osm_file)
    def __load_map_view(self):
        # shortcuts
        filepath = self.view.ask_load_file()
        filename = Path(filepath).stem
        fileext  = Path(filepath).suffix

        if fileext==".osm":
            self.print_msg(f"Loading map: {filename}{fileext}")
            self.map = build_map(filepath)

            ## temp pickling it here since loading takes time
            if not path.exists("cache"):
                mkdir("cache")

            file = open(path.join("cache",f"{filename}.pkl"), "wb")
            pickle.dump(self.map, file)
            file.close()
        elif fileext==".pkl":
            self.print_msg(f"Loading cached map: {filename}{fileext}")
            file = open(filepath, "rb")
            self.map = pickle.load(file)
            file.close()
        else:
            self.print_msg(f"Not a valid map file")
            return

        self.ViewPort = ViewPort(height=self.view.canvas.winfo_height(),
                                 width=self.view.canvas.winfo_width(),
                                 wmin=self.map.min_coord.get_lon_lat(),
                                 wmax=self.map.max_coord.get_lon_lat())

        self.view.draw_places(d_places=self.map.d_places, viewport=self.ViewPort)
        self.view.draw_roads (roads=self.map.main_road, d_nodes=self.map.d_nodes, viewport=self.ViewPort)
        self.map.test_a_star(100)
        self.map.test_parallel_a_star(100, 6)

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
        self.ViewPort.update_scale(self.zoom_in_param)
        self.view.zoom(self.zoom_in_param)

    def on_zoom_out(self):
        self.ViewPort.update_scale(self.zoom_out_param)
        self.view.zoom(self.zoom_out_param)

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



if __name__ == "__main__":
    crtl = Controller()
    crtl.use_view()
    crtl.main_loop()
