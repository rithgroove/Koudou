from src.model.behavioral.module import Module
class EvacuationModule(Module):

	def __init__(self, distance, share_information_chance):
		self.distance = distance
		self.share_information_chance = share_information_chance

	def step(self,kd_sim,kd_map,ts,step_length,rng):
		if (kd_sim.get_attribute("evacuation")):
			for node_id in kd_sim.d_agents_by_location:
				node = kd_map.d_nodes[node_id]
				#collect all connected agents
				agents = kd_sim.d_agents_by_location[node_id].copy()
				for connected_node_id in node.connections:
					agents.extend(kd_sim.d_agents_by_location[connected_node_id])

				#separate to people who knows and doesn't knows evac point
				sources = []
				recipients = []

				for agent in agents: 
					if active_agents.get_attribute("target_evac").lower == "none":
						recipients.append(agent)
					else:
						sources.append(agent)

				#spread the knowledge
				for source in sources:
					for recipient in recipients:
						if rng.uniform(0.0,1.0) > share_information_chance:
							recipients.set_value("target_evac",source.get_attribute("target_evac"))


		# don't forget to check if the agent reached evacuation points
