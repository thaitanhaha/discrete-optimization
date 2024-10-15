# Vehical Routing Problem

## Introduction

The Vehicle Routing Problem is a problem of finding a set of routes for a fleet of vehicles that minimizes travel time. 

The Vehicle Routing Problem can be thought of as multiple Travelling Salesman Problems combined together.

## Mathematics

Let: 
- $N$ be the number of customers.
- $V$ be the number of vehicles.
- $dist_{i,j}$ be distance between customer $i$ and customer $j$.
- $d_i$ be the demand of customer $i$.
- $c$ be the vehicle capacity.
- $x_{i,v}$ be the binary decision variable, which is $1$ if customer $i$ is served by vehicle $v$, and $0$ otherwise.

Hence, the **constraints** are:
- Capacity Constraints: <p align="center"> 
$\sum_{i \in \text{ set of customers served by vehicle }v} d_{i} \leq c, \forall v \in \{0,1,...,V-1\}$ </p>


- Routing Constraints: <p align="center">
$\sum_{v=0}^{V-1} x_{i,v} = 1, \forall i \in \{0,1,...,N-1\}$
</p>

- Flow Conservation: <p align="center">
$\sum_{j=0}^{N-1} x_{i,j} = \sum_{j=0}^{N-1} x_{j,i}, \forall i \in \{0,1,...,N-1\}$
</p>

And the **objective** is <p align="center">
$\min \sum_{v=0}^{V-1}\left(dist_{0,1} + \sum_{i=1}^{N-2}dist_{i, i+1} + dist_{N-1, 0} \right)$
</p>

## Approaches

### Trivial

Customers are prioritized and sorted in descending order of their demand, ensuring that higher-demand customers are assigned first. 

### Local Search

The code is bases on https://github.com/pgrandinetti/discreteopt/tree/master/vrp.

It tries to improve the tour by reversing segments. It computes whether the new tours has a shorter total length after the swap.

If the swap reduces the total tour length, the new tours is accepted; otherwise, it continues checking.

