from src.model.behavioral.module import Module
class EvacuationModule(Module):

	def __init__(self, distance, share_information_chance):
		self.distance = distance
		self.share_information_chance = share_information_chance


		self.triggered = False

	# def setup_default_knowledge(kd_map,kd_sim,value,rng):
	# 	agent_that_know_evacuation_center = value * len(kd_sim.agents)
	# 	temp = kd_sim.agents.copy()
	# 	rng.shuffle(temp)
	# 	for i in range(0,agent_that_know_evacuation_center):
	# 		temp[i].set_attribute("target_evac",kd_map.get_closest_evacuation_center)


	def step(self,kd_sim,kd_map,ts,step_length,rng,logger):
		if (kd_sim.get_attribute("evacuation")):
			if not self.triggered:
				self.triggered = True
				for agent in kd_sim.agents:
					agent.force_reset()
			for node_id in kd_sim.d_agents_by_location:
				node = kd_map.d_nodes[node_id]
				#collect all connected agents
				agents = kd_sim.d_agents_by_location[node_id].copy()
				for connected_node_id in node.connections:
					if (connected_node_id in kd_sim.d_agents_by_location.keys()):
						agents.extend(kd_sim.d_agents_by_location[connected_node_id])

				#separate to people who knows and doesn't knows evac point
				sources = []
				recipients = []

				for agent in agents: 
					if agent.get_attribute("target_evac").lower == "none":
						recipients.append(agent)
					else:
						sources.append(agent)

				#spread the knowledge
				for source in sources:
					for recipient in recipients:
						if rng.uniform(0.0,1.0) > share_information_chance:
							recipients.set_value("target_evac",source.get_attribute("target_evac"))
							recipients.set_value("explored_evac",source.get_attribute("explored_evac"))
							recipients.set_attribute("know_evac",True)

			for evac_center_id in kd_map.d_evacuation_centers:
				evac_center =  kd_map.d_evacuation_centers[evac_center_id]
				capacity = int(evac_center.evacuation_attr["capacity"])
				count = 0
				evacuated = 0 
				unevacuated = []
				if (evac_center.centroid in kd_sim.d_agents_by_location.keys()):
					for agent in kd_sim.d_agents_by_location[evac_center.centroid]:
						if (agent.get_attribute("evacuated") == True):
							evacuated += 1
						else:
							unevacuated.append(agent)
					can_accept = capacity-evacuated
					count = 0
					for agent in unevacuated:
						temp = agent.get_attribute("explored_evac").lower()
						if (temp == "none"):
							temp = ""
						else:
							temp += ","
						temp += f"{evac_center_id}"
						agent.set_attribute("explored_evac", temp) 
						if (count < can_accept):
							agent.set_attribute("evacuated",True)
						agent.set_attribute("know_evac",True)
						count += 1


		# don't forget to check if the agent reached evacuation points
