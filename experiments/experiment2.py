import numpy as np
from typing import List
from utils.enums import Z2, Prop, Logic
from utils.types import Interpretation, Connection
from src.BeliefBase import BeliefBase
from src.MarkovChain import MarkovChain
from src.Graph import Graph


def experiment2():
    """
    CONJECTURE: For each agent in a graph, the number of most frequent
    models after many iterations will always be less than or equal to
    the number of models that might be adopted after a single iteration
    of the distance-based rule. In this way, the Markov Chain analysis
    narrows the space of reasonable collective judgments.
    :return:
    """
    models: List[Interpretation] = [
        [Z2(0), Z2(0), Z2(0), Z2(0), Z2(0)],
        [Z2(1), Z2(1), Z2(1), Z2(1), Z2(1)],
        [Z2(1), Z2(0), Z2(1), Z2(0), Z2(1)],
        [Z2(0), Z2(1), Z2(0), Z2(1), Z2(0)],
    ]
    connections: List[Connection] = []
    agents: List[Interpretation] = [
        [Z2(0), Z2(0), Z2(0), Z2(0), Z2(0)],
        [Z2(1), Z2(1), Z2(1), Z2(1), Z2(1)],
        [Z2(1), Z2(0), Z2(1), Z2(0), Z2(1)],
        [Z2(0), Z2(1), Z2(0), Z2(1), Z2(0)],
    ]
    G: Graph = Graph(models, connections, agents)
    G.complete_graph()

    M: MarkovChain = MarkovChain(G)
    print(M.coord_matrix)

    print('After one iteration, each agent can adopt any one of the models:')
    print(M.update_from_state(M.coord_matrix))

    print('After many iterations, we can possibly converge to any of the following states:')
    for prob, state in M.get_result_by_state():
        print('Probability: ', prob)
        print('State: ', state)

    print('Every outcome in this case is a model of all zeros and all ones, with equal probability for each agent.')
    print('So, in a sense, we have restricted the space of outcomes for each agent from 5 to 2.')

experiment2()