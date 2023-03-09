def get_window_resolution(root, window_width, window_height):
    # If a width contains a "%", the window size is relative to the screen size
    # if it contains only a int, its an absolute value
    width = get_resolution_from_str_and_int(root, window_width)
    height = get_resolution_from_str_and_int(root, window_height)

    return (width, height)


def get_resolution_from_str_and_int(root, var):
    if isinstance(var, str) and var[-1] == "%":
        scale = int(var[:-1])/100
        return root.winfo_screenwidth() * scale
    elif isinstance(var, int):
        return var
    else:
        print("window resolution should be an int or a percentage")
        raise

def get_center_screen(root, window_size):
    # get the screen dimension
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # find the center point
    center_x = int(screen_width/2 - window_size[0]/2)
    center_y = int(screen_height/2 - window_size[1]/2)

    return center_x, center_y

def make_geometry_string(root, window_size):
    center_x, center_y = get_center_screen(root, window_size)
    return f"{window_size[0]}x{window_size[1]}+{center_x}+{center_y}"