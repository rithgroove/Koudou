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
        if current in path:
            raise RecursionError("Found loop on path")
        path.append(current)
        current = came_from[current]
    path.append(start)  
    path.reverse()  
    return path

def get_ordered_tuple(a, b):
    first = min(a, b)
    second = max(a, b)
    return (first, second)

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
    start_goal_tuple = get_ordered_tuple(start_node_id, goal_node_id)

    while not frontier.empty():
        current: str = frontier.get()

        if current == goal_node_id:
            break

        # Checking for cache

        t = get_ordered_tuple(current, goal_node_id)
        if t in cache_dict:
            #print("found in cache")
            cached_path = cache_dict[t]
            if cached_path[0] == goal_node_id:
                cached_path.reverse()
            
            path = reconstruct_path(came_from, start_node_id, current)
            path = path + cached_path[1:]

            cache_dict[start_goal_tuple] = path

            return path

        current_node = kd_map.d_nodes[current]
        for conn in current_node.connections:
            conn_node = kd_map.d_nodes[conn]
            conn_lat_lon = conn_node.coordinate.get_lat_lon()

            first = min(current_node.id, conn_node.id)
            second = max(current_node.id, conn_node.id)
            t = (first, second)
            dist = kd_map.d_roads[t].length

            new_cost = cost_so_far[current] + dist
            if (conn not in cost_so_far or new_cost < cost_so_far[conn]):
                cost_so_far[conn] = new_cost
                dist_to_goal = goal_node.coordinate.calculate_distance(*conn_lat_lon)
                priority = new_cost + dist_to_goal
                frontier.push(conn, priority)
                came_from[conn] = current

    if goal_node_id not in came_from:
        return None

    path = reconstruct_path(came_from, start_node_id, goal_node_id)

    cache_dict[start_goal_tuple] = path
    
    return path


def a_star_thread(thread_id, kd_map, thread_paths, report, results_dict, cache_dict={}):
    #print("starting thread ", thread_id)
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


def parallel_a_star(kd_map, start_goals_arr, n_threads=1, pathfind_cache = {}, report=None):
    """
    [Function] parallel_a_start
    This function performs the A* algorithm for an array of starting and ending points. It can also
    perform the computation usinng multiple processors.

    Parameter:
        - kd_map:   (Map) The map object that contain information about the nodes and roads 
        - start_goals_arr: (List[Tuple[str, str]]) An array that contain tuples, each tuple represent the pair (starting, goal) nodes
        - n_threads: Optional(int) The number of threads to be used by this function
        - report:   Optional(int) the interval for the report of each thread, None is if you do not want any report

    Return:
        - Dict[Tuple[str, str], List[str]]: A dictionary with the paths calculated by the algorithms, the key is the tuple (starting, goal) nodes and
                                            the value is an array of strings that is the path between the nodes
    """
    response = {}
    n_threads = min(n_threads, len(start_goals_arr))
    if n_threads <= 8:
        a_star_thread(0, kd_map, start_goals_arr, report, response, pathfind_cache)
    else:
        thread_paths = np.array_split(start_goals_arr, n_threads)

        with Manager() as manager:
            cache_dict = manager.dict()
            path_dict = manager.dict()
            
            for k, v in pathfind_cache.items():
                cache_dict[k] = v

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
                
            for k, v in cache_dict.items():
                pathfind_cache[k] = v

    return response
