from utils.enums import Z2, Prop, Logic
from src.BeliefBase import BeliefBase
from src.MarkovChain import MarkovChain
from src.Graph import Graph

def run_experiment():
    """
    CONJECTURE: For each agent in a graph, the number of most frequent
    models after many iterations will always be less than or equal to
    the number of models that might be adopted after a single iteration
    of the distance-based rule. In this way, the Markov Chain analysis
    narrows the space of reasonable collective judgments.

    DESCRIPTION: Simple graph example presented in thesis as example.

    FINDINGS: Yes. After many iterations, the most frequent belief for all
    of the 3 agents is the belief (0, 0, 1), where each agent could adopt
    one or more beliefs after a single iteration of the update rule. 
    """
    K = BeliefBase(
        [Prop.P, Prop.Q, Prop.R],
        [[Logic.IFF, Prop.R, Logic.IMPLIES, Prop.P, Prop.Q]]
    )
    G = Graph(K,
        [(0, 0), (0, 1), (0, 2), (1, 1), (1, 0), (2, 2)],
        [
              [Z2(1), Z2(0), Z2(0)],
              [Z2(1), Z2(1), Z2(1)],
              [Z2(0), Z2(0), Z2(1)]
        ]
    )
    M = MarkovChain(G)

    # ugly printing
    print(M.get_result_by_state())

run_experiment()