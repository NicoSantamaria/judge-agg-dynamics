# judge-agg-dynamics
Python library for Markov Chain analysis of constrained belief propagation through 
social networks of rational agents. For more information on the theoretical background
and purpose of the library, see [^1]
[link to my thesis once I've put it online somewhere]. 

## Installation

Working on it!

## Overview

The library provides three classes representing useful objects in the study of the propagation of beliefs through 
communities of rational agents: `BeliefBase`, `Graph`, and `MarkovChain`. The library also makes use of three custom 
enums throughout:

- `Z2` represents an element in the ring of integers modulo 2, and computes the addition, multiplication, and 
negation operations appropriately. For example:
```python
>>> from utils.enums import Z2
>>>
>>>
>>> x = Z2(1)
>>> y = Z2(0)
>>> x + y
Z2.ONE
>>> x * y
Z2.ZERO
>>> x + x
Z2.ZERO
```
- `Prop` represents an atomic proposition.
- `Logic` represents a logical operation.

The `Prop` and `Logic` can be used together to compose complex propositional sentences, whose models can be expressed as 
lists of the `Z2` enum.

Next, we will describe each custom class with code snippets to better understand their behavior. 

### BeliefBase

The `BeliefBase` represents an agenda with an arbitrary set of integrity constraints in accordance with the description 
of belief bases provided in [^2]. Using the `BeliefBase` class, users can provide atomic propositions and propositional 
sentences constructed from those atoms to serve as integrity constraints. Propositional sentences should be expressed 
in Polish notation, with each logical operation preceding its arguments. The `BeliefBase` class then computes the 
set of models for that constrained agenda. 

For example, consider the libel example [^1] [^3] with the agenda $X={p, q, r}$ and the set of integrity constraints 
$I = {r \Leftrightarrow (p \wedge q)}$. We can then use the `BeliefBase` class to compute the set of models representing 
rational judgments of the agenda.

```python
>>> from utils.enums import Z2, Prop, Logic
>>> from src.BeliefBase import BeliefBase
>>>
>>>
>>> props = [Prop.P, Prop.Q, Prop.R]
>>> constraints = [
...     [Logic.IFF, Prop.R, Logic.AND, Prop.P, Prop.Q]
... ]
>>> K = BeliefBase(props, constraints)
>>> K.models
    [Z2.ZERO, Z2.ZERO, Z2.ONE], 
    [Z2.ZERO, Z2.ONE, Z2.ONE], 
    [Z2.ONE, Z2.ZERO, Z2.ZERO], 
    [Z2.ONE, Z2.ONE, Z2.ONE]
]
```

### Graph

The `Graph` class can be used to represent a number of rational agents, their judgments on the agenda, and the connections between them. A `Graph` object can be initialized with either a set of models or an instance of `BeliefBase`, as well as, optionally, agents and connections represented by models and tuples of integers.

```python
>>> from utils.enums import Z2, Prop, Logic
>>> from src.BeliefBase import BeliefBase
>>> from src.Graph import Graph
>>>
>>>
>>> props = [Prop.P, Prop.Q, Prop.Q]
>>> constraints = [
...     [Logic.OR, Prop.P, Prop.Q],
...     [Logic.NOT, Prop.Q]
... ]
>>> K = BeliefBase(props, constraints)
>>> G = Graph(K)
>>> G.models
[
    [Z2.ONE, Z2.ZERO, Z2.ZERO],
    [Z2.ONE, Z2.ONE, Z2.ZERO]
]
```
Or, equivalently:
```python
>>> G = Graph([
...     [Z2.ONE, Z2.ZERO, Z2.ZERO],
...     [Z2.ONE, Z2.ONE, Z2.ZERO]
... ])
>>> G.models
[
    [Z2.ONE, Z2.ZERO, Z2.ZERO],
    [Z2.ONE, Z2.ONE, Z2.ZERO]
]
```
Agents and connections can be provided at the initialization of the object or later through the `add_agent`,
`remove_agent`, `add_connection`, and `remove_connection` methods. Finally, all possible edges can be added to the graph 
with the `complete_graph` method. Accordingly, we can add agents and connections to the graph created in the code 
snippet above:
```python
>>> G.add_agent([Z2.ONE, Z2.ONE, Z2.ZERO])
>>> G.add_agent([Z2.ONE, Z2.ONE, Z2.ZERO])
>>> G.add_agent([Z2.ONE, Z2.ZERO, Z2.ZERO])
>>> G.complete_graph()
>>> G.agents
[
    [Z2.ONE, Z2.ONE, Z2.ZERO], 
    [Z2.ONE, Z2.ONE, Z2.ZERO], 
    [Z2.ONE, Z2.ZERO, Z2.ZERO]
]
>>> G.connections
[
    (0, 0), (0, 1), (0, 2), 
    (1, 0), (1, 1), (1, 2), 
    (2, 0), (2, 1), (2, 2)
]
```
Then, the result of an application of the Hamming distance-based rule can be computed for a specific agent (indexed by 
that agent's position in the graph's list of agents) through the `hamming_distance_rule` method. The 
`hamming_distance_rule` method will return every minimizing model with respect to the judgments of the given agent 
and its connections. A single iteration of update rule on the entire graph can be simulated with the `update` method, 
mutating the object in-place. 
```python
>>> G.hamming_distance_rule(2)
[[Z2.ONE, Z2.ONE, Z2.ZERO]]
>>> G.update()
>>> G.agents
[
    [Z2.ONE, Z2.ONE, Z2.ZERO], 
    [Z2.ONE, Z2.ONE, Z2.ZERO], 
    [Z2.ONE, Z2.ONE, Z2.ZERO]
]
```
In this case, after an iteration of the update rule, the third agent adopts the judgment of its two peers. The `update` 
method breaks ties at random between minimizing models.

### MarkovChain

Using the methodology outlined in Section 3.3.2 of [^1], the `MarkovChain` method provides a number of useful methods 
for the analysis of social networks of rational agents with Markov chains.

An instance of the `MarkovChain` object can be created with an instance of the `Graph` object representing a 
graph $G$ as an argument. The `MarkovChain` class then computes the graph's adjacency matrix $A$, 
the graph state space $\mathcal{S}_G$, the graph state transition matrix $T$, and the stationary matrix with respect 
to the state transition matrix $T$, all of which are available as data attributes to the class. States are represented 
by their respective coordinate matrices, and all matrices are implemented using the `numpy` array type, with 
entries as `Z2` enums where appropriate.

Consider the graph initialized in the above code snippets:
```python
>>> from src.MarkovChain import MarkovChain
>>>
>>>
>>> G.add_agent([Z2.ONE, Z2.ONE, Z2.ZERO])
>>> G.add_agent([Z2.ONE, Z2.ONE, Z2.ZERO])
>>> G.add_agent([Z2.ONE, Z2.ZERO, Z2.ZERO])
>>> G.complete_graph()
>>>
>>> MC = MarkovChain(G)
>>> MC.adjacency
[
    [Z2.ONE Z2.ONE Z2.ONE]
    [Z2.ONE Z2.ONE Z2.ONE]
    [Z2.ONE Z2.ONE Z2.ONE]
]
>>> MC.states
[
    array([
        [Z2.ONE, Z2.ONE, Z2.ONE],
        [Z2.ZERO, Z2.ZERO, Z2.ZERO]
    ], dtype=object), 
    array([
        [Z2.ONE, Z2.ONE, Z2.ZERO],
        [Z2.ZERO, Z2.ZERO, Z2.ONE]
    ], dtype=object), 
    ...,
    array([
        [Z2.ZERO, Z2.ZERO, Z2.ZERO],
        [Z2.ONE, Z2.ONE, Z2.ONE]
    ], dtype=object)
]
>>> MC.state_graph_matrix
[
    [1. 0. 0. 0. 0. 0. 0. 0.]
    [1. 0. 0. 0. 0. 0. 0. 0.]
    [1. 0. 0. 0. 0. 0. 0. 0.]
    [0. 0. 0. 0. 0. 0. 0. 1.]
    [1. 0. 0. 0. 0. 0. 0. 0.]
    [0. 0. 0. 0. 0. 0. 0. 1.]
    [0. 0. 0. 0. 0. 0. 0. 1.]
    [0. 0. 0. 0. 0. 0. 0. 1.]
]
>>> MC.stationary
[
    [1. 0. 0. 0. 0. 0. 0. 0.]
    [1. 0. 0. 0. 0. 0. 0. 0.]
    [1. 0. 0. 0. 0. 0. 0. 0.]
    [0. 0. 0. 0. 0. 0. 0. 1.]
    [1. 0. 0. 0. 0. 0. 0. 0.]
    [0. 0. 0. 0. 0. 0. 0. 1.]
    [0. 0. 0. 0. 0. 0. 0. 1.]
    [0. 0. 0. 0. 0. 0. 0. 1.]
]
```
In this case, no state produces a tie with respect to the Hamming distance-based rule, so the stationary and state 
transition matrices are equivalent. 

It should be noted that the computational complexity of constructing the stationary and state transition matrices 
explodes quickly, so larger agendas and graphs should be handled with care.

## References
[^1]: Nico Santamaria. Judgment aggregation in social networks: a model of deliberative democracy. Thesis Submitted to 
Pomona College, 2025.

[^2]: Gabriella Pigozzi. Belief merging and the discursive dilemma: an argument-based account to paradoxes of judgment 
aggregation. Synthese, 152(2):285–98, 2006.

[^3]: Christian List. The theory of judgment aggregation: An introductory review. Synthese, 187(1):179–207, 2012.