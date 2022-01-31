class ActionWait(Action):
    """
    [Class] ActionWait
    A class that represent agents actions on a building. 
    When this action is processed, the agents will wait for several duration in their last position. 
    
    Properties:
    	- name      : (string-inherited)
        - duration  : (int) duration of wait
        - current   : (int) time spent waiting
    """   
	def __init__(self,name,duration):
        """
        [Constructor]
        Initialize a wait action

        parameter:
        - name     : (string) the name of action (e.g : Eating, Sleeping)
        - duration : (int) the duration of the action in seconds
        """
		super(name)
		self.duration = duration
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
	def is_finished(self):
        """
        [Property]
        Check if this action is finished or not

		return:
		- (bool) true if finished, false otherwise
        """
		return self.current >= self.duration