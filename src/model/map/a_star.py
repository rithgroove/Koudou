import heapq
from os import path
import os
import pickle
import numpy as np
from typing import List, Tuple, Dict
from multiprocessing import Manager, Pool

# Base code and good resource: https://www.redblobgames.com/pathfinding/a-star/implementation.html#optimizations

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return not self.elements

    def push(self, item: str, priority: float):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


def reconstruct_path(came_from: Dict[str, str], start: str, goal: str):
    current: str = goal
    path: List[str] = []
    while current != start:  # note: this will fail if no path is found
        if (current in path):
            print (f"\n\n\n cyclic in {start} to {goal}")
            print (f"\n\n\n current = {current}")
            print (f"\n\n\n came from = {came_from[current]}")
            print(came_from)
            break
        path.append(current)
        current = came_from[current]
    path.append(start)  
    path.reverse()  
    return path


def a_star_search(kd_map, start_node_id: str, goal_node_id: str, cache_dict: Dict[Tuple[str, str], List[str]] = {}):
    """
    [Function] a_star_search
    This function performs the A* algorithm for 2 points

    Parameter:
        - kd_map:   (Map) The map object that contain information about the nodes and roads
        - start_node_id:    (str) the id of the node in the map where the pathfinding starts
        - goal_node_id: (str) the id of the node in the map where the pathfinding should end
        - cache_dict:   Optional(Dict[str, str]) A dictionary with the paths calculated previously by the algorithms, 
                        the key is the tuple (starting, goal) nodes and the value is an array of strings that is the path between the nodes

    Return:
        - List[str] or None : List of IDs representing the path. If there is no path between the nodes, None is returned
    """
    frontier = PriorityQueue()
    frontier.push(start_node_id, 0)

    came_from = {}
    cost_so_far = {}
    came_from[start_node_id] = None
    cost_so_far[start_node_id] = 0

    goal_node = kd_map.d_nodes[goal_node_id]

    while not frontier.empty():
        current: str = frontier.get()

        if current == goal_node_id:
            break

        # Checking for cache
        first = min(current, goal_node_id)
        second = max(current, goal_node_id)
        t = (first, second)
        if t in cache_dict:
            print("found in cache")
            for previous, step in zip(cache_dict[t][:], cache_dict[t][1:]):
                came_from[step] = previous
            break

        current_node = kd_map.d_nodes[current]
        for conn in current_node.connections:
            conn_node = kd_map.d_nodes[conn]
            conn_lat_lon = conn_node.coordinate.get_lat_lon()

            first = min(current_node.id, conn_node.id)
            second = max(current_node.id, conn_node.id)
            t = (first, second)
            dist = kd_map.d_roads[t].length

            new_cost = cost_so_far[current] + dist
            if conn not in cost_so_far or new_cost < cost_so_far[conn]:
                cost_so_far[conn] = new_cost
                dist_to_goal = goal_node.coordinate.calculate_distance(*conn_lat_lon)
                priority = new_cost + dist_to_goal
                frontier.push(conn, priority)
                came_from[conn] = current

    if goal_node_id not in came_from:
        return None

    path = reconstruct_path(came_from, start_node_id, goal_node_id)
    
    first = min(start_node_id, goal_node_id)
    second = max(start_node_id, goal_node_id)
    t = (first, second)
    cache_dict[t] = path
    
    return path


def a_star_thread(thread_id, kd_map, thread_paths, report, results_dict, cache_dict={}):
    print("starting thread ", thread_id)
    for cont, start_goal in enumerate(thread_paths):
        start = start_goal[0] 
        goal = start_goal[1]
        path = a_star_search(kd_map, start, goal, cache_dict)
        results_dict[(start, goal)] = path
        if report is not None and cont%report == 0:
            print(f"Thread {thread_id} finished {cont} paths")

    if report is not None:
        print(f"Thread {thread_id} finished")
    return 


def parallel_a_star(kd_map, start_goals_arr, n_threads=1, cache_file_name = None, report = None):
    """
    [Function] parallel_a_start
    This function performs the A* algorithm for an array of starting and ending points. It can also
    perform the computation usinng multiple processors.

    Parameter:
        - kd_map:   (Map) The map object that contain information about the nodes and roads 
        - start_goals_arr: (List[Tuple[str, str]]) An array that contain tuples, each tuple represent the pair (starting, goal) nodes
        - n_threads: Optional(int) The number of threads to be used by this function
        - cache_file: Optional(str) the name of the file to use as cache, if this file do not exist, it will create a new one and write the results into it
                            please note that at the end of the function, this file is also updated with the new discovered paths
        - report:   Optional(int) the interval for the report of each thread, None is if you do not want any report

    Return:
        - Dict[Tuple[str, str], List[str]]: A dictionary with the paths calculated by the algorithms, the key is the tuple (starting, goal) nodes and
                                            the value is an array of strings that is the path between the nodes
    """
    response = {}
    thread_paths = np.array_split(start_goals_arr, n_threads)

    with Manager() as manager:

        cache_dict = {}
        if cache_file_name != None and os.path.exists(cache_file_name):
            with open(cache_file_name, "rb") as f:
                cache_dict = pickle.load(f)
        cache_dict = manager.dict(cache_dict)
        print(len(cache_dict))
        path_dict = manager.dict()
        tasks = []
        for i in range(n_threads):
            tasks.append((i, kd_map, thread_paths[i], report, path_dict, cache_dict))

        pool = Pool()
        pool.starmap(a_star_thread, tasks)
        pool.close()

        if report is not None:
            print("workers finished, total paths: ", len(path_dict))
        
        for k, v in path_dict.items():
            response[k] = v
            
        if cache_file_name is not None:
            new_cache = {}
            for k, v in cache_dict.items():
                new_cache[k] = v
            with open(cache_file_name, "wb") as f:
                pickle.dump(new_cache, f)

    return response
