from typing import List
from src.jaggdy.utils import Z2
from src.jaggdy.utils import Interpretation, Connection
from src import MarkovChain
from src import Graph


def experiment4():
    """
    CONJECTURE: For each agent in a COMPLETE graph, the number of most frequent
    models after many iterations will always be less than or equal to
    the number of models that might be adopted after a single iteration
    of the distance-based rule. In this way, the Markov Chain analysis
    narrows the space of reasonable collective judgments.

    DESCRIPTION: Complete Graph with highly asymmetric models. would still
    like to induce ties after the first round, but narrow the pool of feasible
    models after many iterations.

    FINDINGS: YES! In fact, this seems to the sort of case I was looking for:
    a complete graph for which, after many iterations, each agent has the
    same most frequent model (in this case, the model of all 1s).
    """
    models: List[Interpretation] = [
        [Z2(0), Z2(0), Z2(0), Z2(0), Z2(0), Z2(0), Z2(0), Z2(0), Z2(0)],
        [Z2(1), Z2(1), Z2(1), Z2(1), Z2(1), Z2(1), Z2(1), Z2(1), Z2(1)],
        [Z2(1), Z2(1), Z2(1), Z2(1), Z2(1), Z2(0), Z2(0), Z2(0), Z2(0)],
        [Z2(0), Z2(0), Z2(0), Z2(0), Z2(1), Z2(1), Z2(1), Z2(1), Z2(1)],
        # [Z2(1), Z2(0), Z2(1), Z2(0), Z2(1), Z2(0), Z2(1), Z2(1), Z2(1)],
    ]
    agents: List[Interpretation] = [
        [Z2(0), Z2(0), Z2(0), Z2(0), Z2(0), Z2(0), Z2(0), Z2(0), Z2(0)],
        [Z2(0), Z2(0), Z2(0), Z2(0), Z2(0), Z2(0), Z2(0), Z2(0), Z2(0)],
        [Z2(1), Z2(1), Z2(1), Z2(1), Z2(1), Z2(1), Z2(1), Z2(1), Z2(1)],
        [Z2(1), Z2(1), Z2(1), Z2(1), Z2(1), Z2(1), Z2(1), Z2(1), Z2(1)],
    ]
    connections: List[Connection] = []
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


experiment4()