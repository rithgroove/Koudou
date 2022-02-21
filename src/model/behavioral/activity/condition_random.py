import operator
from .condition import Condition,_fetch_operator,_fetch_symbols
from src.model.behavioral.attribute.attribute import cast

class ConditionRandom(Condition):
    def __init__(self,name,value,min_value, max_value, operator_string,typing = "string",target ="agent"):
        self.name = name
        self.min_value = cast(min_value,typing)
        self.max_value = cast(max_value,typing)
        self.operator_string = operator_string
        self.operator = _fetch_operator(operator_string)
        self.typing = typing
        self.target = target.lower()
        self.rng = rng

    def check_value(self,agent,kd_sim):
        value2 = self.rng.uniform(self.min, self.max)
        if ("$" in value):
            value = agent.get_attribute(value.replace("$",""))
        value = cast(value,self.typing)
        try:    
            return self.operator(value2, value)
        except:
            tempstring = f"\nProblem with {self.attribute_name}\n"
            tempstring += f"value             = {value}\n"
            if self.target == "agent":
                tempstring += f"agent's attribute = {agent.get_attribute(self.attribute_name)}\n"
            elif self.target == "simulation":
                tempstring += f"agent's attribute = {kd_sim.get_attribute(self.attribute_name)}\n"
            raise ValueError(tempstring)

    @property
    def short_string(self):
        return f"{self.attribute_name} {_fetch_symbols(self.operator_string)} {self.value}"

    def __str__(self):
        tempstring =   "[Condition]\n"
        tempstring += f"  name      = {self.name}\n"
        tempstring += f"  operator  = {self.operator_string}\n"
        tempstring += f"  value     = {self.value}\n\n"
        return tempstring