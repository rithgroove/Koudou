import osmium
from pathlib import Path

from src.view.view import View
from src.model.map.map_manager import build_map


class Controller():
    def __init__(self):
        # view
        self.view = None
        self.map = None

        # bindings
        self.bind_no_view()

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

    ##  ##
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
        filename = self.view.ask_load_file()
        if filename:
            self.print_msg(f"Loading map: {Path(filename).stem}")
            self.map = build_map(filename)

    ## drawing ##


if __name__ == "__main__":
    crtl = Controller()
    crtl.use_view()
    crtl.main_loop()
