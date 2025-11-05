# Abstract

The **Traveling Salesman Problem (TSP)** seeks the shortest possible route visiting each city exactly once and returning to the start.  
As an NP-hard problem, exact algorithms become impractical for large instances.  
This work implements and analyzes three hill-climbing heuristics — **2-city swap**, **2-opt edge reversal**, and **1-city insertion** — using **nearest-neighbor initialization** and **random restarts**.  
The results demonstrate that the 2-opt heuristic consistently dominates, achieving near-optimal tours (as close as 0.7% from the optimum) while maintaining scalability through sampled neighborhoods for instances with \( n \ge 150 \).

---

## 1. Algorithmic Overview

### 1.1 State Representation

A tour is modeled as an ordering of \( n \) cities:

$$
	au = [c_0, c_1, \ldots, c_{n-1}]
$$

representing a cyclic permutation of all nodes.  
Since rotation or reversal does not change the geometry of the tour, the number of unique states is approximately:

$$
rac{(n-1)!}{2}
$$

---

### 1.2 Cost Function

The total tour length is defined as:

$$
f(	au) = \sum_{i=0}^{n-1} d(c_i, c_{(i+1) mod n})
$$

where

$$
d(p, q) = \left\lfloor \sqrt{(x_p - x_q)^2 + (y_p - y_q)^2} 
ight
ceil
$$

follows the **TSPLIB rounding rule**.

---

### 1.3 Initialization — Nearest Neighbor

Starting from a random city, each step appends the closest unvisited city until all are visited.  
This greedy seed construction runs in \( O(n^2) \) time.

---

### 1.4 Neighborhood Structures

1. **Swap (i, j):** exchange two cities  
   Count: \( inom{n}{2} = rac{n(n-1)}{2} \)

2. **2-opt:** reverse the path segment between two edges  
   Count: \( inom{n}{2} - n \)

3. **Insertion (i, j):** remove a city and reinsert elsewhere  
   Count: \( n(n-1) \)
