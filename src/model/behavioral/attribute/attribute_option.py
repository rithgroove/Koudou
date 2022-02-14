from .attribute import Attribute

class AttributeOption(Attribute):
    def __init__(self,name, value,options):
        super(AttributeOption,self).__init__(name,value)
        self.options = options

    def get_options(self):
        return options

    def set_max(self):
        pass

    def set_min(self):
        pass

    def step(self,kd_sim,kd_map,ts,step_length,rng,agent):
        pass