parameters = {
    ""
    
    "SIM_CONFIG":{
        "condition" : ["config/behavioral/condition.csv",
                       "config/evacuation/condition_evac.csv",
                       "config/infection/condition_infection.csv"],

        "default_behavior" : "normal",

        "attributes" : {
            "basic"      : ["config/behavioral/attributes/attribute_basic.csv",
                            "config/evacuation/attributes/attribute_basic_evac.csv"],
            "option"     : ["config/behavioral/attributes/attribute_option.csv",
                            "config/evacuation/attributes/attribute_option_evac.csv"],
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
