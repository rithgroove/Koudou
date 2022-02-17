from .attribute import Attribute

class AttributeOption(Attribute):
    def __init__(self,name, value,options, typing = "string"):
        super(AttributeOption,self).__init__(name,value,typing)
        self.options = options
        for option in self.options:
            option["value"] = self._cast_value(option["value"],self.typing) #cast the options just to ensure

    def get_options(self):
        return options

    def set_value(self,value):
        temp_value = self._cast_value(value,self.typing)
        success = False
        for x in self.options:
            if (x["value"] == temp_value):
                self.value = temp_value
                success = True
        if not success:
            tempstring = "\nInvalid value:\n"
            tempstring += self._get_object_details()
            tempstring += f" {temp_value} is not available in options.\n"
            tempstring += " Available options:\n"
            for option in options:
                tempstring += f" - {option["value"]}\n"
            raise(ValueError(tempstring))

    def step(self,kd_sim,kd_map,ts,step_length,rng,agent):
        pass

    def __str__(self):
        tempstring = "[AttributeOption]\n"
        tempstring += self._get_object_details()
        tempstring += " Options:\n"
        for option in options:
            tempstring += f" - {option["value"]}\n"
