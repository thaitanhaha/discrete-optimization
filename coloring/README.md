# Graph Coloring

## Introduction

Graph coloring refers to the problem of coloring vertices of a graph in such a way that no two adjacent vertices have the same color.

## Mathematics

Let: 
- $n$ be the number of nodes in the graph.
- $x_{i,j}$ be a binary decision variable that equals $1$ if node $i$ is assigned color $j$, and $0$ otherwise.
- $y_{j}$ be a binary decision variable that equals $1$ if color $j$ is used, and $0$ otherwise.

Hence, the **constraints** are:
- Each node must be assigned exactly one color: <p align="center">
$\sum_{j=0}^{n-1} x_{i,j} = 1, \forall i \in \{0,1,...,n-1\}$
</p>

- Adjacent nodes cannot share the same color: <p align="center">
$x_{i,k} + x_{j,k} \leq 1, \forall (i,j) \in \text{graph}, \forall k \in \{0,1,...,n-1\}$
</p>

- A color is used if and only if at least one node is assigned that color: <p align="center">
$x_{i,j} \leq y_j, \forall i \in \{0,1,...,n-1\}, \forall j \in \{0,1,...,n-1\}$
</p>

And the **objective** is <p align="center">
$\min \sum_{j=0}^{n-1} y_j$
</p>

## Approaches

### Greedy 

The algorithm colors one node at a time, always choosing the smallest available color for the current node.

### DSatur (Degree of Saturation)

It works by prioritizing nodes based on their "saturation degree", which refers to the number of distinct colors assigned to their neighboring nodes. 

### Welsh Powell

It prioritizes nodes based on their degree (number of edges).

### DOcplex

``DOcplex`` is a Python library provided by IBM to model and solve optimization problems.

Using this approach, we have to use the **constraints** and **objective** mentioned to code.

### OR-Tools

```OR-Tools``` is an open-source software suite developed by Google for solving optimization problems. 

With this approach, we can just use the constraint that the nodes connected by an edge are assigned different colors (``variables[u]`` $\ne$ ``variables[v]``).


