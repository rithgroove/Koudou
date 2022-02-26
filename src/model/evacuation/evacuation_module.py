from src.model.behavioral.module import Module
class EvacuationModule(Module):

    def __init__(self, distance, share_information_chance):
        self.distance = distance
        self.share_information_chance = share_information_chance


        self.triggered = False

    # def setup_default_knowledge(kd_map,kd_sim,value,rng):
    #     agent_that_know_evacuation_center = value * len(kd_sim.agents)
    #     temp = kd_sim.agents.copy()
    #     rng.shuffle(temp)
    #     for i in range(0,agent_that_know_evacuation_center):
    #         temp[i].set_attribute("target_evac",kd_map.get_closest_evacuation_center)

    # triggered once when the evacuation begin
    def reset_agents_actions(self,kd_sim):
        self.triggered = True
        for agent in kd_sim.agents:
            agent.force_reset()

    #Share ERI (Evacuation Route Information)
    def share_info(self,kd_sim,kd_map,ts,step_length,rng,logger):
        sources = {}
        recipients = {}
        for agent in kd_sim.agents: 
            node_id = agent.get_attribute("current_node_id")
            if agent.get_attribute("know_evac") == True:
                if node_id not in sources.keys():
                    sources[node_id] = []
                sources[node_id].append(agent)
            else:
                if node_id not in recipients.keys():
                    recipients[node_id] = []
                recipients[node_id].append(agent)

        for node_id in sources:
            current_sources = sources[node_id]
            current_recipients = []
            if node_id in recipients.keys():
                current_recipients.extend(recipients[node_id])
            node = kd_map.d_nodes[node_id]
            for conn in node.connections:
                if conn in recipients.keys():
                    current_recipients.extend(recipients[conn])
            for source in current_sources:
                for recipient in current_recipients:
                    if rng.uniform(0.0,1.0,1)[0] > self.share_information_chance:
                        recipient.set_attribute("target_evac",source.get_attribute("target_evac"))
                        recipient.set_attribute("explored_evac",source.get_attribute("explored_evac"))
                        recipient.set_attribute("know_evac",True)

    # mark agents that arrived at evacuation point as evacuated
    def evacuate(self,kd_sim,kd_map,ts,step_length,rng,logger):
        for evac_center_id in kd_map.d_evacuation_centers:
            evac_center =  kd_map.d_evacuation_centers[evac_center_id]
            capacity = int(evac_center.evacuation_attr["capacity"])
            count = 0
            evacuated = 0 
            unevacuated = []
            if (evac_center.centroid in kd_sim.d_agents_by_location.keys()): #check if there are some agents in the evacuation point
                for agent in kd_sim.d_agents_by_location[evac_center.centroid]:
                    if (agent.get_attribute("evacuated") == True): #gather unevacuated agents and count the evacuated one
                        evacuated += 1 
                    else:
                        unevacuated.append(agent)
                for agent in unevacuated:
                    # add this evacuation center to agent's visit history
                    temp = agent.get_attribute("explored_evac").lower()
                    if (temp == "none"):
                        temp = ""
                    else:
                        temp += ","                        
                    temp += f"{evac_center_id}"
                    agent.set_attribute("explored_evac", temp) 
                    agent.set_attribute("know_evac",True)
                    if (evacuated < capacity):        
                        agent.set_attribute("evacuated",True)
                        agent.set_attribute("location","Evacuation_Point")
                        evacuated += 1
                    else:
                        target = kd_map.get_closest_evacuation_center(agent.coordinate,agent.get_attribute("explored_evac"))
                        agent.set_attribute("target_evac",target.centroid)


    # triggered once when the evacuation begin
    def step(self,kd_sim,kd_map,ts,step_length,rng,logger):
        if (kd_sim.get_attribute("evacuation")):
            if not self.triggered:
                #reset agent activities
                self.reset_agents_actions(kd_sim)
            self.share_info(kd_sim,kd_map,ts,step_length,rng,logger)
            self.evacuate(kd_sim,kd_map,ts,step_length,rng,logger)
