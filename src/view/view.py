import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as tk_fdialog
#
# from .draw import ViewPort

class View():
    def __init__(self, window_size=(1024, 768)):
        ### todo: move widget styles to style_config file ###
        my_style = {"bg_btn": "white",
                    "font_btn": "sans 10 bold",
                    "bg_log": "white",
                    "font_log": "sans 10 bold"}
        bg_btn,font_btn,bg_log,font_log ="white","sans 10 bold","white","sans 10 bold"
        ### ###

        ## todo redo ##
        self.scale         = 100000
        self.view_port     = (0,0)
        self.prev_position = None
        ## ##

        self.window_size = self.get_window_resolution(window_size[0], window_size[1])

        # root
        self.root = tk.Tk()
        #self.root.configure(background="black")
        self.root.title("Community Simulator")
        self.root.geometry(self.make_geometry_string(window_size))
        self.root.resizable(False, False)

        ## main bar and notebooks
        self.frame_bar = ttk.Frame(self.root)
        self.frame_nb = ttk.Notebook(self.root)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=39)

        self.frame_bar.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.frame_nb.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.buttons = {}
        ##### main bar #####
        self.buttons["map_load"] = tk.Button(self.frame_bar, bg=bg_btn, font=font_btn, text="Load Map")
        for i in range(4):
            self.buttons[f"null{i}"]  = tk.Button(self.frame_bar, bg=bg_btn, font=font_btn, text=f"null_{i}")

        for i, (key,val) in enumerate(self.buttons.items()):
            self.frame_bar.columnconfigure(i, weight=1)
            self.buttons[key].grid(row=0, column=i, sticky=(tk.N, tk.S, tk.E, tk.W))

        ##### notebook tabs #####
        self.tab1 = ttk.Frame(self.frame_nb)
        self.tab2 = ttk.Frame(self.frame_nb)
        self.frame_nb.add(self.tab1, text='Main')
        self.frame_nb.add(self.tab2, text ='Settings')

        #### notebook tab 1
        self.tab1.frame_canvas = tk.Frame(self.tab1)
        self.canvas = tk.Canvas(self.tab1.frame_canvas)

        # tab 1: canvas pack and size
        self.canvas.pack(expand=True)
        self.canvas.config(width=self.window_size[0], height=self.window_size[1])

        self.tab1.frame_canvas.pack(expand=True)

        ##
        self.load_drawing_methods()

    ## main methods ##
    def main_loop(self):
        self.root.mainloop()
    def close(self):
        self.root.destroy()
    def load_drawing_methods(self):
        #self.draw = Draw(canvas=self.canvas)
        #self.draw_map = self.draw.draw_map(map)
        pass

    ## dialog methods
    def ask_load_file(self):
        filename = tk_fdialog.askopenfilename()
        return filename

    # canvas zooming and mouse_hold (temp)
    def zoom(self, scale):
        self.scale *=  scale
        self.canvas.scale('all', 0, 0, scale, scale)


    ## drawing methods
    def draw_places(self, map, vp):
        for id, place in map.d_places.items():
            place = place.render_info

            # path_trans = [vp.apply(*c.get_lon_lat()) for c in p.coords]
            # path_flat = [e for c in path_trans for e in c]
            # clat, clon = vp.apply(*p.center.get_lon_lat())
            trans_lon = lambda lon: (lon - self.canvasOrigin[0]) * self.scale + self.view_port[0]
            trans_lat = lambda lat: (self.canvasSize[1]-(lat - self.canvasOrigin[1])) * self.scale + self.view_port[1]

            path = [[trans_lon(c.lon), trans_lat(c.lat)] for c in place.coords]
            path_flat = [e for c in path for e in c]
            clat, clon = trans_lon(place.center.lon), trans_lat(place.center.lat)

            if "building" in place.tags.keys():
                if len(path_flat)>=6:
                    #print(f"drawing {id} {path_flat[:4]}")
                    self.canvas.create_polygon(path_flat, outline=place.outline, fill=place.fill, width=2)
                    r=2
                    self.canvas.create_oval(clat-r, clon-r, clat+r, clon+r, fill="black")
                else:
                    1#print("not renderable")
            elif "natural" in place.tags.keys():
                self.canvas.create_polygon(path_flat, outline=place.outline, fill=place.fill, width=2)
            elif "leisure" in place.tags.keys():
                self.canvas.create_polygon(path_flat, outline=place.outline, fill=place.fill, width=2)
            elif "amenity" in place.tags.keys():
                self.canvas.create_polygon(path_flat, outline=place.outline, fill=place.fill, width=2)
            # elif 'highway' in place.tags.keys():
            #     for (lon_a, lat_a), (lon_b, lat_b) in zip(path[:-1], path[1:]):
            #         self.canvas.create_line(lon_a, lat_a, lon_b, lat_b, fill="grey", width=3)
            else:
                pass #note: equivalent to "others" in epidemicon
                #self.canvas.create_polygon(path_flat, outline=place.outline, fill="pink", width=2)

        print("drawing roads")
        print(map.main_road)
        print("====")
        for road in map.main_road:
            lon_a, lat_a = road.location.get_lon_lat()
            lon_a, lat_a = trans_lon(lon_a), trans_lat(lat_a)

            # dont draw twice
            conn_filtered = road.connections[road.connections>road.id]
            for conn_id in conn_filtered:
                lon_b, lat_b = map.d_nodes[conn_id].get_lon_lat()
                lon_b, lat_lat_ba = trans_lon(lon_b), trans_lat(lat_b)
                self.canvas.create_line(lon_a, lat_a, lon_b, lat_b, fill="grey", width=3)


    def draw_path(self, map, vp):
        pass

    ## log ##
    def update_log(self, txt):
        print(txt)
        #todo: widget or tab where we print messages

    ## screen positioning methods ##
    def get_window_resolution(self, window_width, window_height):
        width = 1024
        height = 768

        # If a width contains a "%", the window size is relative to the screen size
        # if it contains only a int, its an absolute value

        if isinstance(window_width, str) and window_width[-1] == "%":
            scale = int(window_width[:-1])/100
            width = self.root.winfo_screenwidth() * scale
        elif isinstance(window_width, int):
            width = window_width

        if isinstance(window_height, str) and window_height[-1] == "%":
            scale = int(window_height[:-1])/100
            height = self.root.winfo_screenheight() * scale
        elif isinstance(window_height, int):
            height = window_height

        return (width, height)
    def get_center_screen(self, window_size):
        # get the screen dimension
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # find the center point
        center_x = int(screen_width/2 - window_size[0]/2)
        center_y = int(screen_height/2 - window_size[1]/2)

        return center_x, center_y
    def make_geometry_string(self, window_size):
        self.center_x, self.center_y = self.get_center_screen(window_size)
        return f"{window_size[0]}x{window_size[1]}+{self.center_x}+{self.center_y}"

if __name__ == "__main__":
    view = View()
    view.main_loop()
