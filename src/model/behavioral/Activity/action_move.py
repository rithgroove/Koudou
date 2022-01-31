class ActionMove(Action):
    """
    [Class] ActionMove
    A class that represent agents move command.
    
    Properties:
    	- name      : (string-inherited)
    """   

	def __init__(self,name,sequence):
        """
        [Constructor]
        Initialize a wait action

        parameter:
        - name     : (string) the name of action (e.g : Eating, Sleeping)
        - duration : (int) the duration of the action in seconds
        """
		super(name)
		self.sequence = sequence

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