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
    print('started!')

    # make this a method in Markov Chain? To find results by input state
    # def get_result_by_state(): ...
    # should accept input by coord_matrix or model matrix
    for i, state in enumerate(M.states):
        if np.array_equal(M.coord_matrix, state):
            end_states = M.stationary[i]
            for j, end_state in enumerate(end_states):
                if end_state != 0:
                    print('Probability:', end_state)
                    print(np.matmul(M.model_matrix, M.states[j]))

run_experiment()