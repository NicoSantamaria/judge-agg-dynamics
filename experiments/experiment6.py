from typing import List
from random import choice
from utils.enums import Z2, Prop, Logic
from utils.types import Sentence, Interpretation, Connection
from src.MarkovChain import MarkovChain
from src.BeliefBase import BeliefBase
from src.Graph import Graph


def experiment6():
    """
    CONJECTURE: For each agent in a COMPLETE graph, the number of most frequent
    models after many iterations will always be less than or equal to
    the number of models that might be adopted after a single iteration
    of the distance-based rule. In this way, the Markov Chain analysis
    narrows the space of reasonable collective judgments.

    DESCRIPTION: Complete graph with larger agenda and number of agents.

    FINDINGS:
    """
    props: List[Prop] = [Prop.P, Prop.Q, Prop.R, Prop.S, Prop.T]
    constraints: List[Sentence] = [
        [Logic.AND, Prop.P, Prop.Q],
        [Logic.IFF, Prop.T, Logic.IMPLIES, Prop.R, Prop.S]
    ]
    K: BeliefBase = BeliefBase(props, constraints)
    G = Graph(K)

    for _ in range(10):
        for _ in range(10):
            G.add_agent(choice(K.models))
        G.complete_graph()
        M = MarkovChain(G)

        print('After one iteration, each agent can adopt any one of the models:')
        print(M.update_from_state(M.coord_matrix))

        print('After many iterations, we can possibly converge to any of the following states:')
        for prob, state in M.get_result_by_state():
            print('Probability: ', prob)
            print('State: ', state)


experiment6()