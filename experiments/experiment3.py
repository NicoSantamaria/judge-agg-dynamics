from typing import List
from src.jaggdy.utils import Z2
from src.jaggdy.utils import Interpretation, Connection
from src import MarkovChain
from src import Graph


def experiment3():
    """
    CONJECTURE: For each agent in a graph, the number of most frequent
    models after many iterations will always be less than or equal to
    the number of models that might be adopted after a single iteration
    of the distance-based rule. In this way, the Markov Chain analysis
    narrows the space of reasonable collective judgments.

    DESCRIPTION: Graph with highly symmetric models to induce
    ties on the first iteration of the distance-based rule. Does the Markov
    Chain method allow us to narrow the space of possible models for each
    agent?

    Same models and number of agents as experiment2, but not complete graph.
    Does removing edges further narrow the number of reasonable models?

    FINDINGS: No. After one iteration, agents 2 and 3 (indexed at 0) can only
    adopt one belief. However, after many iterations, they can adopt
    one of two models with equal probability. However, the total number of
    possible states after many iterations is less than after many.

    Updated conjectures:
        - For complete graphs, the prior conjecture holds
        - the number of total possible states will always be narrowed after many iterations
        than after one.
    """
    models: List[Interpretation] = [
        [Z2(0), Z2(0), Z2(0), Z2(0), Z2(0)],
        [Z2(1), Z2(1), Z2(1), Z2(1), Z2(1)],
        [Z2(1), Z2(0), Z2(1), Z2(0), Z2(1)],
        [Z2(0), Z2(1), Z2(0), Z2(1), Z2(0)],
    ]
    agents: List[Interpretation] = [
        [Z2(0), Z2(0), Z2(0), Z2(0), Z2(0)],
        [Z2(1), Z2(1), Z2(1), Z2(1), Z2(1)],
        [Z2(1), Z2(0), Z2(1), Z2(0), Z2(1)],
        [Z2(0), Z2(1), Z2(0), Z2(1), Z2(0)],
    ]
    connections: List[Connection] = [
        (0, 0), (0, 1), (0, 2), (0, 3),
        (1, 1), (1, 0),
        (2, 2), (2, 3), (2, 0),
        (3, 3), (3, 1), (3, 2),
    ]
    G: Graph = Graph(models, connections, agents)

    M: MarkovChain = MarkovChain(G)
    print(M.coord_matrix)

    print('After one iteration, each agent can adopt any one of the models:')
    print(M.update_from_state(M.coord_matrix))

    print('After many iterations, we can possibly converge to any of the following states:')
    for prob, state in M.get_result_by_state():
        print('Probability: ', prob)
        print('State: ', state)


experiment3()