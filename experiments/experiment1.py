import numpy as np
from utils.enums import Z2, Prop, Logic
from src.BeliefBase import BeliefBase
from src.MarkovChain import MarkovChain
from src.Graph import Graph

def run_experiment():
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