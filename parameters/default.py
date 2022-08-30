parameters = {

    "EXP_NAME":       "default",
    "USE_VIEW":       True,

    # MAP
    "MAP":            "osm_files/TX-To-TU.osm",
    "MAP_CACHE":      "cache/TX-To-TU.pkl",
    "PATHFIND_CACHE": "cache/TX-pathfind.pkl",

    "BUILDING_TAGS":  "config/map/tsukuba-tu-building-data.csv",
    "BUSINESS":       "config/map/business.csv",
    "GRID_SIZE":      10,
    "step_length" : 300,
    "n_agents": 10,
    "sim_config":{
        "condition" : "config/behavioral/condition.csv",
        "default_behavior" : "normal",
        "attributes" : {
            "basic" : ["config/behavioral/attributes/attribute_basic.csv"],
            "option" : ["config/behavioral/attributes/attribute_option.csv"],
            "updateable" : ["config/behavioral/attributes/attribute_updateable.csv"],
            "schedule" : ["config/behavioral/attributes/attribute_schedule.csv"],
            "profession" : ["config/behavioral/profession.csv"]
        },
        "behaviors" :{
            "normal" : "config/behavioral/behavior/behavior_normal.csv",
            "evacuate" : "config/behavioral/behavior/behavior_evacuate.csv"
        }
    }
}
