def AttributeProfession(Attribute):
    """
    [Class] AttributeSchedule
    A class that represent agent's schedule. 
    Think of it as the agent have an appointment.
    
    Properties:
        - name      : (string-inherited) name of the attribute
        - value     : (None) not used
        - schedules : (list-AttributeSchedule) list of work schedule
    """
    def __init__(self, name):
        super(AttributeProfession,self).__init__(name,None)        
        self.schedules = []
           self.active_schedule = None

    def add_schedule(self, schedule):
        self.schedules.append(schedule)

    def get_location(self):
    	self.check_active_schedule()
        if (self.active_schedule is not none):
            return self.active_schedule.location
        return None

    def get_value(self):
        #maybe have a global timestamp variable? 
    	self.check_active_schedule()
        if (self.active_schedule is not none):
            return self.active_schedule.get_value()
        return None

    def check_active_schedule(self):
    	for x in self.schedules:
    		if (x.get_value()):
    			self.active_schedule = x
    			break
