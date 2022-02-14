from .attribute import Attribute

class AttributeGroupedSchedule(Attribute):
    """
    [Class] AttributeGroupedSchedule
    A class that represent agent's schedule. 
    Think of it as the agent have an appointment.
    
    Properties:
        - name      : (string-inherited) "is_working"/ "is_praying" etc
        - value     : (string) the profession name e.g "Student"
        - schedules : (list-AttributeSchedule) list of work schedule
    """
    def __init__(self, name):
        super(AttributeGroupedSchedule,self).__init__(name, "False") 
        self.schedules = []
        self.active_schedule = None

    def add_schedule(self, schedule):
        self.schedules.append(schedule)

    @property
    def get_value(self):
        return self.value

    def step(self,kd_sim,kd_map,ts,step_length,rng,agent):
        self.check_active_schedule()
        self.value = "False"
        for x in self.schedules:
            if (x.get_value == "True"):
                self.value = "True"
                break
    