#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import math
from psutil import cpu_count
from gurobipy import *
from ortools.linear_solver import pywraplp

Point = namedtuple("Point", ['x', 'y'])
Facility = namedtuple("Facility", ['index', 'setup_cost', 'capacity', 'location'])
Customer = namedtuple("Customer", ['index', 'demand', 'location'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)


def ortools(customers, facilities, time_limit=600):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    
    x = [solver.BoolVar(f'x[{i}]') for i in range(len(facilities))]
    y = [[solver.BoolVar(f'y[{i},{j}]') for j in range(len(customers))] for i in range(len(facilities))]
    
    solver.Minimize(
        sum(facilities[i].setup_cost * x[i] for i in range(len(facilities))) +
        sum(length(customers[j].location, facilities[i].location) * y[i][j] for i in range(len(facilities)) for j in range(len(customers)))
    )
    
    # Constraints
    # Each customer assigned to exactly one facility
    for j in range(len(customers)):
        solver.Add(sum(y[i][j] for i in range(len(facilities))) == 1)
    
    # Facility capacity not exceeded
    for i in range(len(facilities)):
        solver.Add(sum(customers[j].demand * y[i][j] for j in range(len(customers))) <= facilities[i].capacity)  
    
    # Customer assigned only to an open facility
    for i in range(len(facilities)):
        for j in range(len(customers)):
            solver.Add(y[i][j] <= x[i])
    
    solver.set_time_limit(time_limit * 1000)
    
    status = solver.Solve()
    
    customer_assignment = [-1] * len(customers)
    total_cost = solver.Objective().Value()
    
    for j in range(len(customers)):
        for i in range(len(facilities)):
            if y[i][j].solution_value() > 0.5:
                customer_assignment[j] = i
                break
    
    solution = f"{total_cost} 0\n"
    solution += ' '.join(map(str, customer_assignment))
    
    return solution

def mip(customers, facilities, time_limit=600):
    model = Model("FacilityLocationProblem")
    
    model.setParam(GRB.Param.TimeLimit, time_limit)

    x = model.addVars(len(facilities), vtype=GRB.BINARY, name="x")
    y = model.addVars(len(facilities), len(customers), vtype=GRB.BINARY, name="y")
    
    model.setObjective(
        quicksum(facilities[i].setup_cost * x[i] for i in range(len(facilities))) + 
        quicksum(length(customers[j].location, facilities[i].location) * y[i, j] for i in range(len(facilities)) for j in range(len(customers))),
        GRB.MINIMIZE
    )
    
    # Constraints
    # Each customer assigned to exactly one facility
    for j in range(len(customers)):
        model.addConstr(quicksum(y[i, j] for i in range(len(facilities))) == 1, name=f"Customer_{j}")
    
    # Facility capacity not exceeded
    for i in range(len(facilities)):
        model.addConstr(quicksum(customers[j].demand * y[i, j] for j in range(len(customers))) <= facilities[i].capacity, name=f"Capacity_{i}")
    
    # Customer assigned only to an open facility
    for i in range(len(facilities)):
        for j in range(len(customers)):
            model.addConstr(y[i, j] <= x[i], name=f"Assign_{i}_{j}") 
    
    model.optimize()
    
    if model.status == GRB.OPTIMAL:
        opt = 1
    else:
        opt = 0

    customer_assignment = [-1] * len(customers)
    total_cost = model.objVal
    
    for j in range(len(customers)):
        for i in range(len(facilities)):
            if y[i, j].X > 0.5:
                customer_assignment[j] = i
                break
    
    solution = f"{total_cost} {opt}\n"
    solution += ' '.join(map(str, customer_assignment))
        
    return solution

def trivial(customers, facilities):
    solution = [-1]*len(customers)
    capacity_remaining = [f.capacity for f in facilities]

    facility_index = 0
    for customer in customers:
        if capacity_remaining[facility_index] >= customer.demand:
            solution[customer.index] = facility_index
            capacity_remaining[facility_index] -= customer.demand
        else:
            facility_index += 1
            assert capacity_remaining[facility_index] >= customer.demand
            solution[customer.index] = facility_index
            capacity_remaining[facility_index] -= customer.demand

    used = [0]*len(facilities)
    for facility_index in solution:
        used[facility_index] = 1

    obj = sum([f.setup_cost*used[f.index] for f in facilities])
    for customer in customers:
        obj += length(customer.location, facilities[solution[customer.index]].location)

    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


def solve_it(input_data):
    lines = input_data.split('\n')

    parts = lines[0].split()
    facility_count = int(parts[0])
    customer_count = int(parts[1])
    
    facilities = []
    for i in range(1, facility_count+1):
        parts = lines[i].split()
        facilities.append(Facility(i-1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3])) ))

    customers = []
    for i in range(facility_count+1, facility_count+1+customer_count):
        parts = lines[i].split()
        customers.append(Customer(i-1-facility_count, int(parts[0]), Point(float(parts[1]), float(parts[2]))))

    output_data = trivial(customers, facilities)
    # output_data = mip(customers, facilities, 600)

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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/fl_16_2)')

