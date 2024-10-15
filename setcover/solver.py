#!/usr/bin/python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2014 Carleton Coffrin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


from collections import namedtuple

from psutil import cpu_count
from gurobipy import *

Set = namedtuple("Set", ['index', 'cost', 'items'])

def set_cover(X, S):
    U = set()
    for i in range(X):
        U.add(i)
    output = []
    while U:
        max_intersection_size = 0
        selected_set_idxs = []
        idx = -1
        for i, s in enumerate(S):
            temp = list(map(int, s.items))
            intersection_size = len(U.intersection(temp))
            if intersection_size > max_intersection_size:
                max_intersection_size = intersection_size
                selected_set_idxs = temp
                idx = i

        if selected_set_idxs == []:
            break
        U = U - set(selected_set_idxs)
        output.append(idx)
    return output

def solve_it_set_cover(input_data):
    lines = input_data.split('\n')

    parts = lines[0].split()
    item_count = int(parts[0])
    set_count = int(parts[1])
    
    sets = []
    for i in range(1, set_count+1):
        parts = lines[i].split()
        sets.append(Set(i-1, float(parts[0]), parts[1:]))

    solve = set_cover(item_count, sets)
    obj = 0
    solution = []
    for s in sets:
        if s.index in solve:
            obj += s.cost
            solution.append(1)
        else:
            solution.append(0)

    output_data = str(obj) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


def solve_it_trivial(input_data):
    lines = input_data.split('\n')

    parts = lines[0].split()
    item_count = int(parts[0])
    set_count = int(parts[1])
    
    sets = []
    for i in range(1, set_count+1):
        parts = lines[i].split()
        sets.append(Set(i-1, float(parts[0]), map(int, parts[1:])))

    solution = [0]*set_count
    coverted = set()
    
    for s in sets:
        solution[s.index] = 1
        coverted |= set(s.items)
        if len(coverted) >= item_count:
            break
        
    obj = sum([s.cost*solution[s.index] for s in sets])

    output_data = str(obj) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


def mip(item_count, sets, verbose=False, num_threads=None, time_limit=None):
    m = Model("set_covering")
    m.setParam('OutputFlag', verbose)
    if num_threads:
        m.setParam("Threads", num_threads)
    else:
        m.setParam("Threads", cpu_count())

    if time_limit:
        m.setParam("TimeLimit", time_limit)

    selections = m.addVars(len(sets), vtype=GRB.BINARY, name="set_selection")

    m.setObjective(LinExpr([s.cost for s in sets], [selections[i] for i in range(len(sets))]), GRB.MINIMIZE)

    m.addConstrs((LinExpr([1 if j in s.items else 0 for s in sets], [selections[i] for i in range(len(sets))]) >= 1
                  for j in range(item_count)),
                 name="ieq1")

    m.update()
    m.optimize()

    soln = [int(var.x) for var in m.getVars()]
    total_cost = int(sum([sets[i].cost * soln[i] for i in range(len(sets))]))

    if m.status == 2:
        opt = 1
    else:
        opt = 0

    return total_cost, opt, soln


from ortools.linear_solver import pywraplp
def ortool(item_count, sets, verbose=False, num_threads=None, time_limit=None):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        raise Exception("Solver not created.")
    
    if verbose:
        solver.EnableOutput()
    else:
        solver.SuppressOutput()

    if num_threads:
        solver.SetNumThreads(num_threads)

    if time_limit:
        solver.SetTimeLimit(time_limit * 1000)

    # Decision variables
    selections = [solver.BoolVar(f'set_selection_{i}') for i in range(len(sets))]

    # Objective function: Minimize the total cost
    objective = solver.Objective()
    for i, s in enumerate(sets):
        objective.SetCoefficient(selections[i], s.cost)
    objective.SetMinimization()

    # Constraints: Each item must be covered at least once
    for j in range(item_count):
        constraint = solver.Constraint(1, solver.infinity(), f'item_constraint_{j}')
        for i, s in enumerate(sets):
            if j in s.items:
                constraint.SetCoefficient(selections[i], 1)

    # Solve the problem
    status = solver.Solve()

    # Extract the solution
    soln = [int(selections[i].solution_value()) for i in range(len(sets))]
    total_cost = sum([sets[i].cost * soln[i] for i in range(len(sets))])

    if status == pywraplp.Solver.OPTIMAL:
        opt = 1
    else:
        opt = 0

    return total_cost, opt, soln


def solve_it(input_data):
    lines = input_data.split('\n')

    parts = lines[0].split()
    item_count = int(parts[0])
    set_count = int(parts[1])
    
    sets = []
    for i in range(1, set_count+1):
        parts = lines[i].split()
        sets.append(Set(i-1, float(parts[0]), set(map(int, parts[1:]))))
    if (set_count <= 1000):
        obj, opt, solution = mip(item_count, sets, verbose=False, time_limit=60)
    else:
        obj, opt, solution = ortool(item_count, sets, verbose=False, time_limit=360)


    output_data = str(obj) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/sc_6_1)')

