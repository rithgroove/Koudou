from .attribute import Attribute
import src.util.global_variable as global_variable

class AttributeSchedule(Attribute):
    """
    [Class] AttributeSchedule
    A class that represent agent's schedule. 
    Think of it as the agent have an appointment.
    
    Properties:
        - name      : (string-inherited) name of the attribute
        - value     : (any:bool-inherited) not used
        - day_str   : (string) name of day in 3 string format ("Mon","Tue","Wed","Thu","Fri","Sat", Sun")
        - start     : (TimeStamp) start time of the schedule
        - end       : (TimeStamp) end time of the schedule
        - repeat    : (bool) default = false. 
                      + If set true, the schedule will be treated as weekly schedule.
                      + If set as false, the schedule will be treated as one off from start and end date (day_str not used)
    """
    def __init__(self, name, start,end, day_str = None,repeat = False):
        super(AttributeSchedule,self).__init__(name,"False")
        self.start = start
        self.end = end
        self.repeat = repeat
        if (repeat and day_str is None):
            raise ValueError("day_str cannot be empty is repeat is True")
        self.day_str = day_str

    @property
    def get_value(self):
        return self.value

    def step(self,kd_sim,kd_map,ts,step_length,rng,agent):
        #maybe have a global timestamp variable? 
        self.value = "False"
        if self.repeat and global_variable.timestamp.get_day_of_week_str() == self.day_str and self.start <= global_variable.timestamp.get_time_only() < self.end:
            self.value = "True"
        elif self.start <= global_variable.timestamp.step_count < self.end:
            self.value = "True"
        else:
            return "False"