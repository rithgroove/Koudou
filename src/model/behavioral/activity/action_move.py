from .action import Action

class ActionMove(Action):
    """
    [Class] ActionMove
    A class that represent agents move command.
    
    Properties:
        - name      : (string-inherited)
    """
    def __init__(self,agent,kd_map,destination_string):
        """
        [Constructor]
        Initialize a wait action

        parameter:
        - name     : (string) the name of action (e.g : Eating, Sleeping)
        - duration : (int) the duration of the action in seconds
        """
        super(ActionMove,self).__init__()
        destination = ""
        temp = destination_string
        temp.replace(")", "")
        typing = "destination_type"
        if ("(" in temp):
            temp2 = temp.split("(")
            temp = temp2[0]
            if (temp2[1].lower() == "destination_id" or temp2[1].lower() == "id"):
                typing = "destination_id"
            elif (temp2[1].lower() == "destination_type" or temp2[1].lower() == "type"):
                typing = "destination_type"
            else:
                raise ValueError("Unknown destination type")
        self.vectors = []

        if typing == "destination_type":
            self.destination = kd_map.get_random_place(temp[0])
        elif typing == "destination_id":
            self.destination = kd_map.get_place_by_id(temp[0])  
        self.sequence = []

    def step(self,kd_sim,kd_map,ts,step_length,rng):
        # if have action do it
        leftover = step_length
        while len(self.actions) > 0:
            act = self.actions[0]
            leftover = act.step(kd_sim,kd_map,ts,step_length,rng)
            if not act.is_finished:
                break
        """
        [Method]
        Update method

        parameter:
        - step_length : (int) how many seconds elapsed

        return:
        - (int) the remainder of the step_length that was not consumed by this action
        """
        return step_length #return the left over time 

    @property
    def is_finished(self):
        """
        [Property]
        Check if this action is finished or not

        return:
        - (bool) true if finished, false otherwise
        """
        return True

    @property
    def short_string(self):
        return f"Move to {self.destination_string}"

    def __str__(self):
        return f"[ActionMove]\n   Destination = {self.destination_string}"