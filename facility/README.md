# Facility Location

## Introduction

Facility location involves determining the optimal locations for facilities to minimize costs, maximize service levels, and enhance efficiency. 

## Mathematics

Let 

- $x_i$ be a binary variable that indicates whether facility $i$ is opened ($x_i=1$) or not ($x_i=0$).
- $y_{ij}$ be a binary variable that indicates whether customer $j$ is assigned to facility $i$ ($y_{ij}=1$) or not ($y_{ij}=0$).
- $C_i$ be the setup cost for facility $i$.
- $d_{ij}$ be the distance between facility $i$ and customer $j$.
- $D_j$ be the demand of customer $j$.
- $C_i^{max}$ be the maximum capacity of facility $i$.

Hence, the **constraints** are:
- Each customer assigned to exactly one facility: <p align="center">
$\sum_{i} y_{ij} = 1, \forall j$
</p>

- Facility capacity not exceeded: <p align="center">
$\sum_{j} D_j \cdot y_{ij} \leq C_i^{max}, \forall i$
</p>

- Customer assigned only to an open facility: <p align="center">
$y_{ij} \leq x_i, \forall i,j$
</p>

And the **objective** is <p align="center">
$\min \sum_{i} C_i \cdot x_i + \sum_i \sum_j d_{ij} \cdot y_{ij}$
</p>


## Approaches

### Greedy

For each customer:

- If the remaining capacity of the current facility can accommodate the customer's demand, the customer is assigned to that facility. 

    The facility's remaining capacity is then decremented by the customer's demand.

- If the current facility cannot accommodate the customer, the function increments facility_index to consider the next facility. 

### OR-Tools

```OR-Tools``` is an open-source software suite developed by Google for solving optimization problems. 

Using this approach, we have to use the **constraints** and **objective** mentioned to code.

### Gurobi

```Gurobi``` is a powerful and widely-used optimization solver designed to solve various types of mathematical programming problems.

Using this approach, we have to use the **constraints** and **objective** mentioned to code.





