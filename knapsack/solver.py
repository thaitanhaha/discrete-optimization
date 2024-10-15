#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from operator import attrgetter

from psutil import cpu_count
from gurobipy import *
Item = namedtuple("Item", ['index', 'value', 'weight', 'density'])


def greedy(capacity, items):
    weight, value = 0,0
    taken = [0]*len(items) 
    for item in sorted(items, key = lambda x: x.value/x.weight, reverse=True):        
        if weight + item.weight <= capacity:
            weight += item.weight
            value += item.value
            taken[item.index] = 1
    return value, taken

def dp(capacity, items):
    n = len(items)
    dp = [[0 for _ in range(n+1)] for _ in range(capacity+1)]
    for i in range(1, n+1):
        v_i = items[i-1].value
        w_i = items[i-1].weight
        for k in range(capacity+1):
            if k < w_i:
                dp[k][i] = dp[k][i-1]
            else:
                dp[k][i] = max(dp[k][i-1], v_i + dp[k-w_i][i-1])
    value = dp[-1][-1]
    taken = []
    for i in reversed(range(1,n+1)):
        w_i = items[i-1].weight
        if dp[k][i] == dp[k][i-1]:
            taken.insert(0,0)
        else:
            k = k-w_i
            taken.insert(0,1)
    
    return value, taken

def mip(cap, items, verbose=False, num_threads=None):
    item_count = len(items)
    values = [item.value for item in items]
    weights = [item.weight for item in items]

    m = Model("knapsack")
    m.setParam('OutputFlag', verbose)
    if num_threads:
        m.setParam("Threads", num_threads)
    else:
        m.setParam("Threads", cpu_count())

    x = m.addVars(item_count, vtype=GRB.BINARY, name="items")
    m.setObjective(LinExpr(values, [x[i] for i in range(item_count)]), GRB.MAXIMIZE)
    m.addLConstr(LinExpr(weights, [x[i] for i in range(item_count)]), GRB.LESS_EQUAL, cap, name="capacity")

    m.update()
    m.optimize()

    opt = 1 if m.status == 2 else 0

    return int(m.objVal), opt, [int(var.x) for var in m.getVars()]


def solve_it(input_data):
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        v, w = int(parts[0]), int(parts[1])
        items.append(Item(i-1, v, w, 1.0 * v / w))

    if (item_count <= 1000) and (capacity < 3000000):
        obj, taken = dp(capacity, items)
    else:
        obj, taken = greedy(capacity, items)
    opt = 0
    output_data = str(obj) + ' ' + str(opt) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

