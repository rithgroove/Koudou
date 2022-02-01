import operator
class Condition:
	def __init__(self,name,value, operator_string):
		name = name
		value = value
		self.operator = _fetch_operator(operator_string)

	def check_value(self,agent)
		return self.operator(agent.get_attribute(self.name), value)

def _fetch_operator(operator_string):
	if(operator_string.lower() == "greater_than_equal")
		return operator.ge
	elif(operator_string.lower() == "greater_than")
		return operator_string.gt
	elif(operator_string == "less_than_equal")
		return operator_string.le
	elif(operator_string == "less_than")
		return operator_string.lt
	elif(operator_string == "equal")
		return operator_string.eq
	elif(operator_string == "not_equal")
		return operator_string.ne