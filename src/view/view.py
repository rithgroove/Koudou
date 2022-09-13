import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as tk_fdialog
import numpy as np

from src.view.draw import Draw

class View():
    def __init__(self, window_size=(1024, 768)):
        ### todo: move widget styles to style_config file ###
        my_style = {"bg_btn": "white",
                    "font_btn": "sans 10 bold",
                    "bg_log": "white",
                    "font_log": "sans 10 bold"}
        bg_btn,font_btn,bg_log,font_log ="white","sans 10 bold","white","sans 10 bold"
        ### ###

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
        self.buttons["sim_run"] = tk.Button(self.frame_bar, bg=bg_btn, font=font_btn, text="Run")
        self.buttons["sim_step"] = tk.Button(self.frame_bar, bg=bg_btn, font=font_btn, text="Step")
        self.buttons["rnd_ag"] = tk.Button(self.frame_bar, bg=bg_btn, font=font_btn, text=f"Random Agent")

        # for i in range(1):
        #     self.buttons[f"null{i}"]  = tk.Button(self.frame_bar, bg=bg_btn, font=font_btn, text=f"null_{i}")

        for i, (key,val) in enumerate(self.buttons.items()):
            self.frame_bar.columnconfigure(i, weight=1)
            self.buttons[key].grid(row=0, column=i, sticky=(tk.N, tk.S, tk.E, tk.W))

        ##### notebook tabs #####
        self.tab1 = ttk.Frame(self.frame_nb)
        self.tab2 = ttk.Frame(self.frame_nb)
        self.frame_nb.add(self.tab1, text='Main')
        self.frame_nb.add(self.tab2, text ='Settings')

        #### notebook tab 1
        self.canvas_frame = tk.Frame(self.tab1)
        self.canvas = tk.Canvas(self.canvas_frame)

        self.zoom_in_btn = tk.Button(self.canvas, text='+', bg=bg_btn, font=font_btn)
        self.zoom_in_btn.place(relx= .95, rely=.01)
        self.zoom_out_btn = tk.Button(self.canvas, text='-', bg=bg_btn, font=font_btn)
        self.zoom_out_btn.place(relx= .95, rely=.01, y=self.zoom_in_btn.winfo_height()+20)
        self.coord_label = tk.Label(self.canvas, text="", fg="Red", font=("Helvetica", 12), background="White")
        self.coord_label.place(relx=.01, rely=.95)

        self.clock = tk.Label(self.canvas, text="", fg="Green", font=("Helvetica", 18), background="White")
        self.clock.place(relx=.01, rely=.01)


        ### tab 2

        # tab 1: canvas pack and size
        self.canvas.pack(expand=True)
        self.canvas.config(width=self.window_size[0], height=self.window_size[1])

        self.canvas_frame.pack(expand=True)
        self.draw = Draw(canvas=self.canvas)


    ## main methods ##
    def main_loop(self):
        self.root.mainloop()
    def close(self):
        self.root.destroy()

    ## dialog methods
    def ask_load_file(self):
        filename = tk_fdialog.askopenfilename()
        return filename

    # canvas zooming and mouse_hold (temp)
    def zoom(self, scale):
        self.canvas.scale('all', 0, 0, scale, scale)




    def update_view(self):
        pass

    def btn_start_change_method(self, text, method):
        self.buttons["sim_run"]["text"]    = text
        self.buttons["sim_run"]["command"] = method


        self.buttons["sim_step"]["state"] = tk.NORMAL
        if text == "Pause": # auto-running
            self.buttons["sim_step"]["state"] = tk.DISABLED

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
