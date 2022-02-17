import warnings

class Attribute:

    def __init__(self,name,value,typing = "string"):
        self.name = name
        self.value = self._cast(value)
        self.typing = typing.lower()
        if (self.typing == "integer"):
            self.typing = "int"
        self._cast_value()

    @property
    def get_value(self):
        return self.value

    def set_value(self,value):
        temp_value = self._cast(value)
        self.value = temp_value

    def update_value(self,value):
        if self.typing == "int" || self.typing == "integer" || self.typing == "float":
            self.value += value
        else:
            tempstring = "[Attribute] this attribute cannot be updated:\n"
            tempstring += self._get_object_details()
            tempstring = "Only integer or float type are updatable.\n"
            tempstring = "Use set_value(value) for other type.\n"
            raise(ValueError(tempstring))

    def set_max(self):
        tempstring = "[Attribute] setting max value failed:\n"
        tempstring += self._get_object_details()
        tempstring += "set max value is not available for this attribute.\n"
        warnings.warn(tempstring)

    def set_min(self):
        tempstring = "[Attribute] setting min value failed:\n"
        tempstring += self._get_object_details()
        tempstring += "set min value is not available for this attribute.\n"
        warnings.warn(tempstring)

    def step(self,kd_sim,kd_map,ts,step_length,rng,agent):
        self._cast_value() # just to make sure the data is safe

    def _get_object_details(self):
        tempstring =  f"   attribute   : {self.name}\n"
        tempstring += f"   type        : {self.typing}\n"
        tempstring += f"   value       : {self.value}\n"
        return tempstring

    def _cast_value(self):
        try:
            self._value =  self._cast(self.value,self.typing)
        except ValueError as e:
            if ("[Attribute] " in str(e)):
                raise ValueError(e)
            else:
                tempstring = f"\nUnable to cast value to {self.typing} :\n"
                tempstring += self._get_object_details()
                raise(ValueError(tempstring))

    def _cast(self,value,typing):
        if typing == "string":
            return f"{value}"
        elif self.typing == "bool":
            return bool(value)
        elif self.typing == "int" || typing == "integer":
            return int(value)
        elif self.typing == "float":
            return int(value)
        else:
            tempstring = "\n[Attribute] Unknown typing for:\n"
            tempstring += self._get_object_details()
            raise(ValueError(tempstring))

    def __str__(self):
        tempstring = "[Attribute]\n"
        tempstring += _get_object_details()
        return tempstring

