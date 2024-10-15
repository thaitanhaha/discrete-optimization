# Knapsack

## Introduction

Given a set of items, each with a weight and a value, determine which items to include in the collection so that the total weight is less than or equal to a given limit and the total value is as large as possible.

## Mathematics

Let: 
- $n$ be the number of items.
- $v_i$ be the value of item $i$.
- $w_i$ be the weight of item $i$.
- $C$ be the maximum capacity of the knapsack.
- $x_i \in \{0,1\}$ be a binary variable that indicates whether item $i$ is selected ($1$) or not ($0$).

Hence, the **constraint** is:
- Total weight of the selected items does not exceed the capacity $C$: <p align="center">
$\sum_{i=0}^{n-1} w_{i} \cdot x_{i} \leq C$
</p>

And the **objective** is <p align="center">
$\max \sum_{i=0}^{n-1} v_i \cdot x_i$
</p>

## Approaches

### Greedy 

The items are sorted in descending order based on the value-to-weight ratio (`item.value/item.weight`). 

This ratio is used because items with a higher value per unit of weight are more "valuable" in terms of the knapsack's limited capacity.

### Dynamic Programming

$dp$: A table where $dp[k][i]$ holds the maximum value that can be obtained with a capacity $k$ using the first $i$ items. 

This $dp$ has dimensions $(C + 1) × (n + 1)$ where $n$ is the number of items.

The main algorithm:

```
for i in range(1, n+1):
    v_i = items[i-1].value
    w_i = items[i-1].weight
    for k in range(capacity+1):
        if k < w_i:
            dp[k][i] = dp[k][i-1]
        else:
            dp[k][i] = max(dp[k][i-1], v_i + dp[k-w_i][i-1])
```

- If the current item's weight is greater than the capacity ($k < w_i$), it can't be added, so the value remains the same as without the item ($dp[k][i-1]$).

- Otherwise, chooses the maximum value between 
    - Not including the current item: $dp[k][i-1]$
    - Including the current item: $v_i + dp[k-w_i][i-1]$

The final result is $dp[C][n]$

### Gurobi

```Gurobi``` is a powerful and widely-used optimization solver designed to solve various types of mathematical programming problems.

Using this approach, we have to use the **constraints** and **objective** mentioned to code.




