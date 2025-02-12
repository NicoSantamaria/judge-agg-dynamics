from copy import deepcopy
from Agent import *
from BeliefBase import *
from Graph import *
from typing import *


# IC = BeliefBase(["p", "q", "r"], [["iff", "r", "implies", "p", "q"]])
# K1 = Agent(IC, {"p": 1, "q": 1, "r": 1}, "K1")
# K2 = Agent(IC, {"p": 1, "q": 0, "r": 0}, "K2")
# K3 = Agent(IC, {"p": 0, "q": 0, "r": 1}, "K3")
# G = Graph(IC, [K1, K2, K3])
# G.complete_graph()
# G.remove_connection(K1, K2)

# G.update(G.hamming_distance_rule, G.tiebreaker_chance)

# props = ['p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# I = BeliefBase(props, [
#     ['iff', 'p', 'not', 'z'],
#     ['iff', 'r', 'implies', 'p', 'q'],
#     ['iff', 't', 'and', 'p', 's'],
#     ['iff', 'v', 'and', 'r', 'implies', 'r', 'u'],
#     ['iff', 'x', 'or', 'not', 'u', 'and', 'v', 'w'],
#     ['iff', 'z', 'iff', 'x', 'y'],
# ])

# J1 = Agent(I, dict(zip(props, [1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0])), "J1")
# J2 = Agent(I, dict(zip(props, [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0])), "J2")
# J3 = Agent(I, dict(zip(props, [1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0])), "J3")
# J4 = Agent(I, dict(zip(props, [0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1])), "J4")
# J5 = Agent(I, dict(zip(props, [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0])), "J5")
# J6 = Agent(I, dict(zip(props, [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0])), "J6")
# J7 = Agent(I, dict(zip(props, [0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1])), "J7")
# J8 = Agent(I, dict(zip(props, [0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1])), "J8")
# J9 = Agent(I, dict(zip(props, [0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1])), "J9")
# J10 = Agent(I, dict(zip(props, [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0])), "J10")
# J11 = Agent(I, dict(zip(props, [1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0])), "J11")
# J12 = Agent(I, dict(zip(props, [0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1])), "J12")


# G = Graph(I, [J1, J2, J3, J4, J5, J6, J7, J8, J9, J10, J11, J12])
# G.complete_graph()

# G.update(G.hamming_distance_rule, G.tiebreaker_chance)
# Instant Convergence!

# create a holdout...
# G.graph[J1] = [J1]

# Nothing interesting...

# J1 = Agent(I, dict(zip(props, [1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0])), "J1")
# J2 = Agent(I, dict(zip(props, [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0])), "J2")
# J3 = Agent(I, dict(zip(props, [1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0])), "J3")

# G = Graph(I, [J1, J2, J3])
# G.complete_graph()

# converges immediately

# G = Graph(I, [J1, J2, J3, J4, J5, J6, J7, J8, J9, J10, J11, J12])
# G.add_connections(J1, [J1, J2, J5, J6, J7, J8, J12])
# G.add_connections(J2, [J2, J8, J9, J10, J11])
# G.add_connections(J3, [J1, J2, J3, J4, J5, J6, J7, J8, J9, J10, J11, J12])
# G.add_connections(J4, [J1, J2, J3, J4,  J7, J8, J10, J11, J12])
# G.add_connections(J5, [J1, J2, J5])
# G.add_connections(J6, [J1, J2, J6, J12])
# G.add_connections(J7, [J5, J6, J7, J8, J11, J12])
# G.add_connections(J8, [J2, J3, J4, J5, J6, J7, J8, J9, J10, J11, J12])
# G.add_connections(J9, [J1, J2, J3, J4, J5, J6, J7, J8, J9, J12])
# G.add_connections(J10, [J9, J10, J11, J12])
# G.add_connections(J11, [J4, J5, J6, J7, J8, J11, J12])
# G.add_connections(J12, [J1, J2, J3, J4, J5, J6, J7, J8, J9, J10, J11, J12])

# print(G)

# This one is more interesting, reaches consensus after two iterations


# Conjectures:
# 1. Complete graph: always reaches stable point after one iteration
# 2. Complete graph: for large enough agenda, always reaches consensus after one iteration
# 3. Any graph: always reaches stable point (i.e., there are no cycles)
# 4. Connected graph: for large enough agenda, always reaches consensus

if __name__ == "__main__":
    results = {
        'A': {
            (0, 0, 1) : 0,
            (1, 1, 1): 0,
            (1, 0, 0): 0,
            (0, 1, 1): 0
        }, 
        'B': {
            (0, 0, 1) : 0,
            (1, 1, 1): 0,
            (1, 0, 0): 0,
            (0, 1, 1): 0
        },
        'C': {
            (0, 0, 1) : 0,
            (1, 1, 1): 0,
            (1, 0, 0): 0,
            (0, 1, 1): 0
        }
    }
    props = ['p', 'q', 'r']

    for _ in range(1000):
        I = BeliefBase(props, [['iff', 'r', 'implies', 'p', 'q']])
        J1 = Agent(I, dict(zip(props, [0,0,1])), 'A')
        J2 = Agent(I, dict(zip(props, [1,1,1])), 'B')
        J3 = Agent(I, dict(zip(props, [0,0,1])), 'C')

        G = Graph(I, [J1, J2, J3])
        G.add_connections(J1, [J1, J2, J3])
        G.add_connections(J2, [J1, J2])
        G.add_connections(J3, [J3])

        for _ in range(10):
            G.update()

        for agent in G.graph:
            results[agent.name][agent.models[0]] += 1
            

    print(results)
    # for agent in results:
    #     for model in agent:
    #         print(f"{agent}: {model} -- {results[agent][model]}")
        

# I = BeliefBase(props, [['iff', 'r', 'implies', 'p', 'q']])
# J1 = Agent(I, dict(zip(props, [1,0,0])), 'A')
# J2 = Agent(I, dict(zip(props, [1,1,1])), 'B')
# J3 = Agent(I, dict(zip(props, [0,0,1])), 'C')

# G = Graph(I, [J1, J2, J3])
# G.add_connections(J1, [J1, J2, J3])
# G.add_connections(J2, [J1, J2])
# G.add_connections(J3, [J3])

# G.update()
# print(G)
