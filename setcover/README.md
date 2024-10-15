# Set Cover

## Introduction

Given a number of items and a collection of sets $S_1, S_2,..., S_m$ with corresponding costs $c_1, c_2,..., c_m$ that cover all the items. The goal is to find the sub-collection of these sets with mininum total cost such that their union can still cover all the items. 

## Mathematics

Let: 
- $n$ be the number of items.
- $m$ be the number of sets.
- Each set $S_i$ has a cost $c_i$ and covers a subset of items $T_i$.
- $x_{i}$ be the binary decision variable, which is $1$ if the set $S_i$ is selected, and $0$ otherwise.

Hence, the **constraint** is:

- Each item is covered by at least one selected set: <p align="center">
$\sum_{i \in \mathcal{S} } 1_{j \in S_i} \cdot x_i \geq 1, \forall j \in \{0,1,...,n-1\}$
</p>

And the **objective** is <p align="center">
$\min \sum_{i=0}^{m-1} c_{i} \cdot x_{i}$
</p>

## Approaches

### Trivial

Selecting sets one by one until all items are covered.

### Greedy

Iteratively selecting the subset that covers the maximum number of remaining uncovered items until all items are covered.

### Gurobi

```Gurobi``` is a powerful and widely-used optimization solver designed to solve various types of mathematical programming problems.

Using this approach, we have to use the **constraint** and **objective** mentioned to code.

### OR-Tools

```OR-Tools``` is an open-source software suite developed by Google for solving optimization problems. 

Using this approach, we have to use the **constraint** and **objective** mentioned to code.

