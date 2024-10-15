#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
import datetime
import time
import copy
import random

Customer = namedtuple("Customer", ['index', 'demand', 'x', 'y'])
DEPOT = None

def length(customer1, customer2):
    return math.sqrt((customer1.x - customer2.x)**2 + (customer1.y - customer2.y)**2)

def calculate_cost(vehicle_tours):
    # calculate the cost of the solution; for each vehicle the length of the route
    global DEPOT
    obj = 0
    vehicle_count = len(vehicle_tours)
    for v in range(0, vehicle_count):
        vehicle_tour = vehicle_tours[v]
        if len(vehicle_tour) > 0:
            obj += length(DEPOT, vehicle_tour[0])
            for i in range(0, len(vehicle_tour)-1):
                obj += length(vehicle_tour[i],vehicle_tour[i+1])
            obj += length(vehicle_tour[-1], DEPOT)
    return obj

def accept_neighbor(old, new, random_parameter):
    old_val = calculate_cost(old)
    new_val = calculate_cost(new)
    if new_val <= old_val:
        return True
    if math.exp(-abs(new_val - old_val) / random_parameter) > random.random():
        return True
    return False

def trivial(customers, customer_count, depot, vehicle_count, vehicle_capacity):
    # build a trivial solution
    # assign customers to vehicles starting by the largest customer demands
    vehicle_tours = []
    
    remaining_customers = set(customers)
    remaining_customers.remove(depot)
    
    for v in range(0, vehicle_count):
        vehicle_tours.append([])
        capacity_remaining = vehicle_capacity
        while sum([capacity_remaining >= customer.demand for customer in remaining_customers]) > 0:
            used = set()
            order = sorted(remaining_customers, key=lambda customer: -customer.demand*customer_count + customer.index)
            for customer in order:
                if capacity_remaining >= customer.demand:
                    capacity_remaining -= customer.demand
                    vehicle_tours[v].append(customer)
                    used.add(customer)
            remaining_customers -= used

    return vehicle_tours

def find_neighbor(curr, vehicle_capacity):
    neighbor = copy.deepcopy(curr)
    v1 = random.randint(0, len(curr) - 1)
    while len(curr[v1]) == 0:
        v1 = random.randint(0, len(curr) - 1)
    c1 = random.randint(0, len(curr[v1]) - 1)
    temp = neighbor[v1][c1]
    cap1 = vehicle_capacity + 1
    cap2 = 0

    while cap1 > vehicle_capacity or cap2 < temp.demand:
        v2 = random.randint(0, len(curr) - 1)
        c2 = random.randint(0, len(curr[v2]))
        cap1 = sum(curr[v1][x].demand for x in range(len(curr[v1])) if x != c1)
        if c2 < len(curr[v2]):
            cap1 += curr[v2][c2].demand
        cap2 = vehicle_capacity - sum(curr[v2][x].demand for x in range(len(curr[v2])) if x != c2)

    if c2 < len(curr[v2]):
        neighbor[v1][c1] = neighbor[v2][c2]
        neighbor[v2][c2] = temp
    else:
        neighbor[v1].remove(temp)
        neighbor[v2].insert(c2, temp)
    return neighbor

def local_search(customers, curr, vehicle_capacity):
    best = copy.deepcopy(curr)
    restart = 0
    counter = 0
    T = len(customers)
    alpha = 0.999
    min_T = 1e-8
    start = time.time()
    diff = time.time() - start
    while diff < 600:
        if T <= min_T:
            T = len(customers)
            restart += 1
        neighbor = find_neighbor(curr, vehicle_capacity)
        if neighbor is not None:
            if accept_neighbor(curr, neighbor, T):
                curr = neighbor
                if calculate_cost(curr) < calculate_cost(best):
                    best = copy.deepcopy(curr)
        counter += 1
        T *= alpha
        diff = time.time() - start
    return best


def solve_it(input_data):
    lines = input_data.split('\n')

    parts = lines[0].split()
    customer_count = int(parts[0])
    vehicle_count = int(parts[1])
    vehicle_capacity = int(parts[2])
    
    customers = []
    for i in range(1, customer_count+1):
        line = lines[i]
        parts = line.split()
        customers.append(Customer(i-1, int(parts[0]), float(parts[1]), float(parts[2])))

    # the depot is always the first customer in the input
    depot = customers[0] 
    global DEPOT
    DEPOT = depot

    vehicle_tours = trivial(customers, customer_count, depot, vehicle_count, vehicle_capacity)
    vehicle_tours = local_search(customers, vehicle_tours, vehicle_capacity)

    # checks that the number of customers served is correct
    assert sum([len(v) for v in vehicle_tours]) == len(customers) - 1

    obj = calculate_cost(vehicle_tours)

    # prepare the solution in the specified output format
    outputData = '%.2f' % obj + ' ' + str(0) + '\n'
    for v in range(0, vehicle_count):
        outputData += str(depot.index) + ' ' + ' '.join([str(customer.index) for customer in vehicle_tours[v]]) + ' ' + str(depot.index) + '\n'

    return outputData

import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:

        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/vrp_5_4_1)')

