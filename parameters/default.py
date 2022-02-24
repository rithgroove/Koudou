parameters = {

    "EXP_NAME":       "test_config_file",

    # MAP
    "MAP":            "osm_files/TX-To-TU.osm",
    # "MAP_CACHE":      "cache/TX-To-TU.pkl",
    "PATHFIND_CACHE": "cache/TX-pathfind.pkl",

    "BUILDING_TAGS":  "config/map/tsukuba-tu-building-data.csv",
    "BUSINESS":       "config/map/business.csv",
    "GRID_SIZE":      20,

    "DISEASES": [
        "config/infection/covid.json"
    ],

    "SIM_CONFIG": {
        "condition": "config/behavioral/condition.csv",
        "default_behavior": "normal",
        "attributes": {
            "basic": ["config/behavioral/attributes/attribute_basic.csv"],
            "option": ["config/behavioral/attributes/attribute_option.csv"],
            "updateable": ["config/behavioral/attributes/attribute_updateable.csv"],
            "schedule": ["config/behavioral/attributes/attribute_schedule.csv"],
            "profession": ["config/behavioral/profession.csv"]
        },
        "behaviors": {
            "normal": "config/behavioral/behavior/behavior_normal.csv",
            "evacuate": "config/behavioral/behavior/behavior_evacuate.csv"
        }
    }
}
