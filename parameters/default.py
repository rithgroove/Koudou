parameters = {
    "EXP_NAME":       "test_config_file",
    "MAP":            "osm_files/TX-To-TU.osm",
    "MAP_CACHE":      "cache/TX-To-TU.pkl",
    "PATHFIND_CACHE": "cache/TX-pathfind.pkl",


    "SEED":            101512,
    "N_AGENTS":        2000,
    "THREADS":         10,

    "BUILDING_TAGS":  "config/map/tsukuba-tu-building-data.csv",
    "BUSINESS":       "config/map/business.csv",
    "GRID_SIZE":      20,
    "EVAC_CENTER" :   "config/map/evacuation_center.json",
    "STEP_LENGTH" :   1,#300,
    "MAX_DAYS"    :   49*24*12,


    "DISEASES": ["config/infection/covid.json"],

    "EVACUATION": {"DISTANCE":10, "SHARE_INFO_CHANCE": 0.8},

    "SIM_CONFIG":{
        "condition" : ["config/behavioral/condition.csv",
                       "config/evacuation/condition_evac.csv",
                       "config/infection/condition_infection.csv"],

        "default_behavior" : "normal",

        "attributes" : {
            "basic"      : ["config/behavioral/attributes/attribute_basic.csv",
                            "config/evacuation/attributes/attribute_basic_evac.csv"],
            "option"     : ["config/behavioral/attributes/attribute_option.csv"],
            "updateable" : ["config/behavioral/attributes/attribute_updateable.csv"],
            "schedule"   : ["config/behavioral/attributes/attribute_schedule.csv"],
            "profession" : ["config/behavioral/profession.csv"]
        },
        "behaviors" :{
            "normal"         : "config/behavioral/behavior/behavior_normal.csv",
            "evacuate"       : "config/evacuation/behavior/behavior_evacuate.csv",
            "self_isolation" : "config/infection/behavior/behavior_symptomatic.csv",
            "severe"         : "config/infection/behavior/behavior_severe.csv"
        }
    }
}
