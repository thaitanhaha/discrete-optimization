#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from time import time
from collections import namedtuple
from itertools import combinations, permutations, chain
from gurobipy import Model, GRB, quicksum
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import numpy as np

locations = []

def construct_distance_matrix(locations):
    loc_array = np.array(locations)
    num_locations = loc_array.shape[0]
    distances = {}
    for from_index in range(num_locations):
        distance_vector = np.linalg.norm(loc_array[from_index] - loc_array, axis=1)
        distances[from_index] = {to_index: int(distance * 1000) for to_index, distance in enumerate(distance_vector)}
    return distances

def solve_it_ortools(input_data):
    lines = input_data.split('\n')
    locations = []
    for line in lines[1:-1]:
        node1, node2 = line.split()
        locations.append((float(node1), float(node2)))

    distance_matrix = construct_distance_matrix(locations)

    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), 1, 0)

    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()

    # search_parameters.first_solution_strategy = (
    #     routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.seconds = 15
    search_parameters.log_search = False

    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        index = routing.Start(0)
        plan_output = ''
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += '{} '.format(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)

        output_data = f"{solution.ObjectiveValue() / 1000.0} {0}\n"
        output_data += f"{plan_output[:-1]}"
        return output_data



def edge_length(points, v1, v2):
    p1 = points[v1]
    p2 = points[v2]
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def cycle_length(points, cycle):
    return sum(edge_length(points, v1, v2) for v1, v2 in zip(cycle[:-1], cycle[1:]))

def check_solution(points, cycle):
    return len(set(cycle[:-1])) == len(points) == len(cycle) - 1

def swap(points, cycle, obj, start, end):
    improved = False
    new_cycle = cycle[:start] + cycle[start:end + 1][::-1] + cycle[end + 1:]
    new_obj = obj - \
              (edge_length(points, cycle[start - 1], cycle[start]) +
               edge_length(points, cycle[end], cycle[end + 1])) + \
              (edge_length(points, new_cycle[start - 1], new_cycle[start]) +
               edge_length(points, new_cycle[end], new_cycle[end + 1]))
    
    if new_obj < obj:
        return new_cycle, new_obj, True
    return cycle, obj, improved

def solve_2_opt(points, t_threshold=None, return_cycle=False):
    cycle = list(range(len(points))) + [0]
    obj = cycle_length(points, cycle)
    
    improved = True
    start_time = time()
    
    while improved:
        if t_threshold and time() - start_time >= t_threshold:
            break
        improved = False
        for start, end in combinations(range(1, len(cycle) - 1), 2):
            cycle, obj, improved = swap(points, cycle, obj, start, end)
            if improved:
                break
    
    if return_cycle:
        return cycle[:-1]
    
    if not check_solution(points, cycle):
        raise ValueError("Solution not valid")
    
    return "{:.2f} {}\n{}".format(obj, 0, ' '.join(map(str, cycle[:-1])))

Point = namedtuple("Point", ['x', 'y'])

def solve_it(input_data):
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount + 1):
        line = lines[i]
        parts = line.split()
        points.append((float(parts[0]), float(parts[1])))

    output_data = solve_2_opt(points, t_threshold=600)
    return output_data
    

import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

