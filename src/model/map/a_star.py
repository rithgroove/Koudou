import heapq
import numpy as np
from typing import List, Tuple, Dict, Optional
from multiprocessing import Process, Manager, Pool

# Base code and good resource: https://www.redblobgames.com/pathfinding/a-star/implementation.html#optimizations

class PriorityQueue:
    def __init__(self):
        self.elements: List[Tuple[float, str]] = []

    def empty(self):
        return not self.elements

    def push(self, item: str, priority: float):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


def reconstruct_path(came_from: Dict[str, str], start: str, goal: str):
    current: str = goal
    path: List[str] = []
    while current != start:  # note: this will fail if no path found
        path.append(current)
        current = came_from[current]
    path.append(start)  # optional
    path.reverse()  # optional
    return path

def a_star_search(kd_map, start_node_id: str, goal_node_id: str):
    frontier = PriorityQueue()
    frontier.push(start_node_id, 0)

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
            if conn not in cost_so_far or new_cost < cost_so_far[conn]:
                cost_so_far[conn] = new_cost
                dist_to_goal = goal_node.coordinate.calculate_distance(*conn_lat_lon)
                priority = new_cost + dist_to_goal
                frontier.push(conn, priority)
                came_from[conn] = current

    if goal_node_id not in came_from:
        return None

    return reconstruct_path(came_from, start_node_id, goal_node_id)


def a_star_thread(args):
    thread_id, kd_map, thread_paths, report, results_dict = args
    print("starting thread ", thread_id)
    for cont, start_goal in enumerate(thread_paths):
        start = start_goal[0] 
        goal = start_goal[1]
        path = a_star_search(kd_map, start, goal)
        results_dict[(start, goal)] = path
        if report is not None and cont%report == 0:
            print(f"Thread {thread_id} finished {cont} paths")

    if report is not None:
        print(f"Thread {thread_id} finished")
    return 


def parallel_a_star(kd_map, start_goals_arr, n_workers=1, report=None):
    response = {}
    thread_paths = np.array_split(start_goals_arr, n_workers)

    with Manager() as manager:
        path_dict = manager.dict()
        pool = Pool()

        tasks = []
        for i in range(n_workers):
            tasks.append((i, kd_map, thread_paths[i], report, path_dict))

        pool.map(a_star_thread, tasks)
        pool.close()

        if report is not None:
            print("workers finished, total paths: ", len(path_dict))
        
        for k, v in path_dict:
            response[k] = v
            
    return response
