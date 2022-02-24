from .action import Action
from .movement_vector import MovementVector
class ActionMove(Action):
    """
    [Class] ActionMove
    A class that represent agents move command.
    
    Properties:
        - name      : (string-inherited)
    """
    def __init__(self,agent,kd_map,destination_string,rng):
        """
        [Constructor]
        Initialize a wait action

        parameter:
        - name     : (string) the name of action (e.g : Eating, Sleeping)
        - duration : (int) the duration of the action in seconds
        """
        super(ActionMove,self).__init__()
        self.destination = ""
        temp = destination_string
        temp =temp.replace(")", "")
        self.destination_string = destination_string
        self.sequence = []
        self.agent = agent
        self.finished = False
        self.origin = agent.get_attribute("current_node_id")
        self.vectors = []
        self.target = None
        if destination_string != "!evac":
            node = kd_map.d_nodes[self.origin]
            self.target = kd_map.get_closest_evacuation_center(node.coordinate,agent.get_attribute("explored_evac"))
            self.destination = self.target.centroid
        elif destination_string != "!random":
            self.destination = kd_map.get_random_connected_nodes(self.origin,agent.get_attribute("last_node_id"),rng)
        else:
            typing = "destination_type"
            if ("(" in temp):
                temp2 = temp.split("(")
                temp = temp2[0]
                if (temp2[1].lower() == "destination_id") or (temp2[1].lower() == "id"):
                    typing = "destination_id"
                elif (temp2[1].lower() == "destination_type") or (temp2[1].lower() == "type"):
                    typing = "destination_type"
                else:
                    raise ValueError(f"Unknown destination type : {temp2[1].lower()}")
    
            if ("$" in temp):
                temp = agent.get_attribute(temp.replace("$",""))

            if typing == "destination_type":
                self.destination = kd_map.get_random_business(temp, 1, rng)[0].node_id
            elif typing == "destination_id":
                self.destination = temp

    def force_reset(self):
        self.vectors = [self.vectors[0]]

    def step(self,kd_sim,kd_map,ts,step_length,rng):
        # if have action do it
        leftover = step_length
        while len(self.sequence) > 0:
            mov_vec = self.sequence[0]
            leftover = mov_vec.step(self.agent,leftover,kd_map) 
            if not mov_vec.is_finished:
                break
            else:
                self.sequence.pop(0)
        if len(self.sequence) == 0:
            self.finished = True
        return leftover

    @property
    def is_finished(self):
        """
        [Property]
        Check if this action is finished or not

        return:
        - (bool) true if finished, false otherwise
        """
        return self.finished

    @property
    def short_string(self):
        return f"Move to {self.destination_string}"

    def __str__(self):
        tempString = f"[ActionMove]\n"
        tempString += f"   Origin = {self.origin}\n"
        tempString += f"   Destination = {self.destination}\n"
        tempString += f"   Destination String = {self.destination_string}"
        return tempString

    def generate_vector(self,kd_map,path):
        working = None
        for x in path:
            temp = kd_map.get_node(x)
            if working is not None:
                self.sequence.append(MovementVector(working,temp))
            working = temp


