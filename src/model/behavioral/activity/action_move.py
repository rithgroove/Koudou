from .action import Action

class ActionMove(Action):
    """
    [Class] ActionMove
    A class that represent agents move command.
    
    Properties:
        - name      : (string-inherited)
    """
    def __init__(self,destination_string):
        """
        [Constructor]
        Initialize a wait action

        parameter:
        - name     : (string) the name of action (e.g : Eating, Sleeping)
        - duration : (int) the duration of the action in seconds
        """
        super(ActionMove,self).__init__()
        self.destination_string = destination_string
        self.sequence = []

    def update(self,step_length):
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