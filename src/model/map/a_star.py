import heapq
from collections import List, Tuple, Dict, Optional
from .map import Map

# Base code and good resource: https://www.redblobgames.com/pathfinding/a-star/implementation.html#optimizations

class PriorityQueue:
    def __init__(self):
        self.elements: List[Tuple[float, str]] = []

    def empty(self) -> bool:
        return not self.elements

    def push(self, item: str, priority: float):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> str:
        return heapq.heappop(self.elements)[1]


def reconstruct_path(came_from: Dict[str, str], start: str, goal: str) -> List[str]:

    current: str = goal
    path: List[str] = []
    while current != start:  # note: this will fail if no path found
        path.append(current)
        current = came_from[current]
    path.append(start)  # optional
    path.reverse()  # optional
    return path

def a_star_search(kd_map: Map, start_node_id: str, goal_node_id: str):
    frontier = PriorityQueue()
    frontier.put(start_node_id, 0)

    came_from: Dict[str, Optional[str]] = {}
    cost_so_far: Dict[str, float] = {}
    came_from[start_node_id] = None
    cost_so_far[start_node_id] = 0

    goal_node = kd_map.d_nodes[goal_node_id]

    while not frontier.empty():
        current: str = frontier.get()

        if current == goal_node_id:
            break
        
        c_node = kd_map.d_nodes[current]
        for conn in c_node.connections:
            conn_node = kd_map.d_nodes[conn]
            conn_lat_lon = conn_node.coordinate.get_lat_lon()
            # When we have the Road obj, this value will be stored in the object
            dist = c_node.coordinate.calculate_distance(*conn_lat_lon)
            new_cost = cost_so_far[current] + dist
            if conn not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[conn] = new_cost
                dist_to_goal = goal_node.coordinate.calculate_distance(conn_lat_lon)
                priority = new_cost + dist_to_goal
                frontier.put(conn, priority)
                came_from[conn] = current

    if goal_node_id not in came_from:
        return None

    return reconstruct_path(came_from, start_node_id, goal_node_id)
