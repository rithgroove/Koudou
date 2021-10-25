import osmium
from src.model.map.node import Node
from src.model.map.way import Way
class MapHandler(osmium.SimpleHandler):
	def __init__(self):
		osmium.SimpleHandler.__init__(self)
		self.nodes = []
		self.nodesDict = {}
		self.ways = []
		
	def node(self, n):
		"""
		[Method] node
		Do not use this method, this is an override method from osmium to generate nodes.
		"""
		temp =  Node()
		temp.fill(n)
		self.nodesDict[f"n{n.id}"] = temp
		self.nodes.append(temp)
		
	def way(self, n):
		"""
		[Method] way
		Do not use this method, this is an override method from osmium to generate ways.
		"""
		temp =  Way()
		temp.fill(n,self.nodesDict)
		#self.waysDict[f"n{n.id}"] = temp
		self.ways.append(temp)

	def __str__(self):
		temp_string = "[MapHandler]\n"
		temp_string += f"Nodes = {len(self.nodes)}\n"
		temp_string += f"Ways = {len(self.ways)}"
		return temp_string
		# temp_string = "Nodes : \n"
		# for x in self.nodes:
		# 	temp_string += x.__str__()
		# temp_string += "\n\nway\n\n"
		# for x in self.ways:
		# 	temp_string += x.__str__()
		# return tempstring