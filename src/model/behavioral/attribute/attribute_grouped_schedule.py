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
        #maybe have a global timestamp variable? 
        self.check_active_schedule()
        if (self.active_schedule is not None):
            return self.active_schedule.get_value
        return "False"

    def check_active_schedule(self):
        for x in self.schedules:
            if (x.get_value == "True"):
                self.active_schedule = x
                break
