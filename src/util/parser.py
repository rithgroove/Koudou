from platform import system

def load_parameters(filename):
    parameters = load_defaults()

    if filename is None:
        return parameters

    with open(filename, 'r') as file:
        tmp_params = "".join(file.readlines())

    ctx = {"parameters": dict()}
    try:
        exec(tmp_params, ctx)
    except SyntaxError:
        raise Exception("Invalid syntax in the parameter file.")

    for key in ctx["parameters"].keys():
        parameters[key] = ctx["parameters"][key]

    return parameters

def load_defaults():
    parameters = {

        "EXP_NAME": "default",

        "MAP":               None,
        "MAP_CACHE":         None,
        "PATHFIND_CACHE":    None,
        "BUILDING_TAGS":     None,
        "BUSINESS":          None,
        "GRID_SIZE":         20,

        "USE_VIEW":         False,
        "ZOOM_IN":          1.1,
        "ZOOM_OUT":         (10.0/11.0),

        "OS": system(),
        "step_length": 300,
        "n_agents": 16,

    }
    return parameters
