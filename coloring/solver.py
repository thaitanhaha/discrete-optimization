#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import OrderedDict
from ortools.sat.python import cp_model

def greedy_coloring(graph, node_count):
    result = [-1] * node_count
    result[0] = 0

    available_colors = [False] * node_count

    for u in range(1, node_count):
        for neighbor in graph[u]:
            if result[neighbor] != -1:
                available_colors[result[neighbor]] = True
        color = 0
        while color < node_count and available_colors[color]:
            color += 1
        result[u] = color
        for neighbor in graph[u]:
            if result[neighbor] != -1:
                available_colors[result[neighbor]] = False
    return result


def welsh_powell(graph, node_count):
    degree = [(len(graph[node]), node) for node in range(node_count)]
    degree.sort(reverse=True, key=lambda x: x[0])
    sorted_nodes = [node for _, node in degree]

    color_assignment = [-1] * node_count
    current_color = 0

    for node in sorted_nodes:
        if color_assignment[node] == -1:
            color_assignment[node] = current_color
            for neighbor in sorted_nodes:
                if neighbor != node and color_assignment[neighbor] == -1:
                    # Check if the neighbor can be colored with the current color
                    if all(color_assignment[adj] != current_color for adj in graph[neighbor]):
                        color_assignment[neighbor] = current_color
            current_color += 1

    return color_assignment


def dsatur(graph, node_count):
    color_assignment = [-1] * node_count
    degree = [len(graph[node]) for node in range(node_count)]
    saturation_degree = [0] * node_count

    def max_saturation_vertex():
        max_saturation = -1
        max_degree = -1
        selected_vertex = -1
        for vertex in range(node_count):
            if color_assignment[vertex] == -1:
                if (saturation_degree[vertex] > max_saturation or
                    (saturation_degree[vertex] == max_saturation and degree[vertex] > max_degree)):
                    max_saturation = saturation_degree[vertex]
                    max_degree = degree[vertex]
                    selected_vertex = vertex
        return selected_vertex

    for _ in range(node_count):
        vertex = max_saturation_vertex()
        neighbor_colors = {color_assignment[neighbor] for neighbor in graph[vertex] if color_assignment[neighbor] != -1}
        color = 0
        while color in neighbor_colors:
            color += 1
        color_assignment[vertex] = color
        for neighbor in graph[vertex]:
            if color_assignment[neighbor] == -1:
                unique_neighbor_colors = {color_assignment[adj] for adj in graph[neighbor] if color_assignment[adj] != -1}
                saturation_degree[neighbor] = len(unique_neighbor_colors)

    return color_assignment


from docplex.mp.model import Model
def solve_model(graph, node_count):
    model = Model(name="Graph Coloring")
    n = node_count
    x = {(i, j): model.binary_var(name=f"x_{i}_{j}") for i in range(n) for j in range(n)}
    y = {j: model.binary_var(name=f"y_{j}") for j in range(n)}

    for i in range(n):
        model.add_constraint(model.sum(x[i, j] for j in range(n)) == 1)

    for i in range(n):
        for j in graph[i]:
            if i < j:
                for k in range(n):
                    model.add_constraint(x[i, k] + x[j, k] <= 1)

    for j in range(n):
        for i in range(n):
            model.add_constraint(x[i, j] <= y[j])

    model.minimize(model.sum(y[j] for j in range(n)))

    solution = model.solve()

    colors = {i: j for i in range(n) for j in range(n) if solution[x[i, j]] == 1}

    num_colors_used = sum(solution[y[j]] for j in range(n))
    return num_colors_used, colors

from ortools.sat.python import cp_model
def or_solver(node_count, edges):
    solved = False
    max_color = 1

    while not solved:
        max_color += 1
        model = cp_model.CpModel()
        variables = [model.NewIntVar(0, max_color-1, f'x{i}') for i in range(node_count)]
        for edge in edges:
            model.Add(variables[edge[0]] != variables[edge[1]])

        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 30.0
        status = solver.Solve(model)

        if status == cp_model.FEASIBLE:
            solved = True
            solution = [solver.Value(var) for var in variables]

    return max_color, solution


def improve_with_or_solver(items, node_count, target, time_limit=10):
    model = cp_model.CpModel()
    colors = [
        model.NewIntVar(0, node_count - 1, 'c%i' % i) for i in range(node_count)
    ]
    max_color = model.NewIntVar(0, node_count - 1 ,'obj')

    for u,v in items:
        model.Add(colors[u] != colors[v])

    model.AddMaxEquality(max_color, colors)

    model.Add(colors[0] == 0)
    for i in range(node_count):
        model.Add(colors[i] <= i+1)

    model.Add(max_color <= target)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.Solve(model)

    try:
        results = [solver.Value(colors[i]) for i in range(node_count)]
    except IndexError:
        results = None

    return results


def solve_it(input_data):
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    graph = [[] for _ in range(node_count)]
    items = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        graph[int(parts[0])].append(int(parts[1]))
        graph[int(parts[1])].append(int(parts[0]))
        items.append(list(map(int, parts)))

    colors = dsatur(graph, node_count)

    if node_count <= 75:
        target = max(colors)
        while True:
            new_colors = improve_with_or_solver(items, node_count, target, time_limit=300)
            if new_colors is not None:
                colors = new_colors
                target -= 1
            else:
                break

    max_color = max(colors) + 1
    output_data = f"{max_color} {0}\n"
    output_data += ' '.join(map(str, colors))

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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

