# Traveling Salesman Problem

## Introduction

The problem is to find the shortest possible route that visits every city exactly once and returns to the starting point.

## Mathematics

Let: 
- $n$ be the number of cities.
- $d_{i,j}$ be distance (or cost) between city $i$ and city $j$.
- $x_{i,j}$ be the binary decision variable, which is $1$ if the tour goes directly from city $i$ to city $j$, and $0$ otherwise.
- $u_i$ be the number of cities visited before city $i$ in the tour.

Hence, the **constraints** are:
- Visit each city once: 

    First <p align="center"> 
$\sum_{j=0}^{n-1} x_{i,j} = 1, \forall i \in \{0,1,...,n-1\}$ </p>

    and <p align="center"> 
$\sum_{i=0}^{n-1} x_{i,j} = 1, \forall j \in \{0,1,...,n-1\}$ </p>

- Subtour Elimination: To prevent subtours (disconnected loops), one common method is to use the Miller-Tucker-Zemlin (MTZ) formulation: <p align="center">
$u_i - u_j + n \cdot x_{i,j} \leq n-1, \forall i \ne j$
</p>

And the **objective** is <p align="center">
$\min \sum_{i=0}^{n-1}\sum_{j=0}^{n-1} d_{i,j} \cdot x_{i,j}$
</p>

## Approaches

### Local Search 2-opt

The code is bases on https://github.com/jixinfeng/discopt-soln/tree/master/week-04-tsp. 

It tries to improve the tour by reversing segments (swapping city pairs) within the tour. It computes whether the new tour has a shorter total length after the swap.

If the swap reduces the total tour length, the new tour is accepted; otherwise, it continues checking other possible swaps.

### OR-Tools

```OR-Tools``` is an open-source software suite developed by Google for solving optimization problems. 

In this TSP, we use `OR-Tools Routing Model`.

- **Manager**: `RoutingIndexManager` maps the problem nodes (cities) to indices that the OR-Tools solver understands. It requires the number of nodes, the number of vehicles (1 for TSP), and the starting node (city 0).

- **Model**: `RoutingModel` is the core of the OR-Tools routing library.

- **Distance Callback**: The `distance_callback` function computes the travel cost between two nodes (cities) by referencing the distance matrix.

- **Cost Assignment**: `SetArcCostEvaluatorOfAllVehicles` sets the callback as the cost evaluator, so that every "arc" (path between two cities) is evaluated based on the computed distances.

- **Search Parameters**: The `search_parameters` object is used to configure the solving process.
There are 2 options of `search_parameters`:
    - `FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION`: heuristic, suitable for quick solutions and large datasets
    - `LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH`: metaheuristic, ideal for finding high-quality solutions




