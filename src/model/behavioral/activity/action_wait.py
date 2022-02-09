from .action import Action

class ActionWait(Action):
    """
    [Class] ActionWait
    A class that represent agents actions on a building. 
    When this action is processed, the agents will wait for several duration in their last position. 
    
    Properties:
        - name      : (string-inherited)
        - duration  : (int) duration of wait in seconds
        - current   : (int) time spent waiting
    """   
    def __init__(self,command_string,rng):
        """
        [Constructor]
        Initialize a wait action

        parameter:
        - name     : (string) the name of action (e.g : Eating, Sleeping)
        - duration : (int) the duration of the action in seconds
        """
        super(ActionWait,self).__init__()
        # if "$" in command_string:

        # elif "-" in command_string:

        # else:
        #     self.duration = int

        temp = duration.split("-")
        min = temp[0]
        max = temp[1]
        self.current = 0

    def update(self,step_length):
        """
        [Method]
        Update method

        parameter:
        - step_length : (int) how many seconds elapsed

        return:
        - (int) the remainder of the step_length that was not consumed by this action
        """
        self.current += step_length #add step length to the executable
        self.remainder = max(0,self.current - self.duration) #check is time passed is bigger than the wait duration 
        self.current = min(self.current, self.duration) #if current is bigger than duration set the value of current to duration
        return remainder #return the left over time 

    @property
    def short_string(self):
        return f"Wait for {self.min}-{self.max}minutes"

    def __str__(self):
        tempstring = "[Action-Wait]\n"
        tempstring += f"   Duration = {self.min}-{self.max}minutes"


    @property
    def is_finished(self):
        """
        [Property]
        Check if this action is finished or not

        return:
        - (bool) true if finished, false otherwise
        """
        return self.current >= self.duration

def _fetch_operator(operator_string):
    if(operator_string == "*"):
        return operator.mul
    elif(operator_string == "/"):
        return operator.div
    elif(operator_string == "%"):
        return operator.modulo
    elif(operator_string == "+"):
        return operator.add
    elif(operator_string == "-"):
        return operator.add