import numpy as np
from itertools import product, permutations
from functools import reduce
from Graph import *
from typing import *
from AgentFromModels import *
from GraphFromModels import *
from copy import deepcopy

type Matrix = np.ndarray
type StateGraphMatrix = List[List[int]]
type State = List[Tuple[str, Interpretation]]

class MarkovChain:
    def __init__(self, graph: GraphFromModels):
        self.graph: GraphFromModels = graph
        self.states: List[State] = self.generate_states()
        self.state_graph_matrix: StateGraphMatrix = self.build_state_graph()

    def generate_states(self) -> List[State]:
        # number of states can be easliy computed beforehand, so this can
        # be improved by initializing the list and avoiding the append
        # later on
        states: List[GraphFromModels] = list()
        
        agents_perms = permutations(self.graph.graph)
        models_combos = product(
            self.graph.models, 
            repeat=len(self.graph.graph)
        )
        
        for agents, models in product(agents_perms, models_combos):
            new_state: State = [(agent.name, model) 
                for agent, model in zip(agents, models)
            ]
            states.append(new_state)

        return states
    
    def build_state_graph(self) -> StateGraphMatrix:
        length = len(self.states)
        state_graph_matrix = [[0] * length] * length

        # iterate over the states
        for i, state in enumerate(self.states):
            print(state)

        return state_graph_matrix
    
    # works, as far as I can tell
    def hamming_distance_rule(self, models: List[Interpretation]) -> List[Interpretation]:
        candidates: List[Interpretation] = self.graph.models
        candidate_minimum: float = float('inf')

        for candidate in candidates:
            current_distance: int = 0

            for model in models:
                distance_to_model = self.graph.hamming_distance(candidate, model)
                current_distance += distance_to_model

            if current_distance < candidate_minimum:
                candidates = [candidate]
                candidate_minimum = current_distance
            elif current_distance == candidate_minimum:
                candidates.append(candidate)

        return candidates
    
    
    def fast_exponent(self, mat: Matrix) -> Matrix:
        eigenvalues, eigenvectors = np.linalg.eig(mat)
        diagonal = np.diag(eigenvalues)
        trans_matrix_inv = np.linalg.inv(eigenvectors)

        return reduce(np.matmul, [
            eigenvectors, 
            np.linalg.matrix_power(diagonal, 1000), 
            trans_matrix_inv
        ])

    def find_stationary(self, mat: Matrix) -> Matrix:
        eigenvalues, eigenvectors = np.linalg.eig(mat)
        stationary_index = np.where(np.isclose(eigenvalues, 1))[0][0]
        stationary_distribution = eigenvectors[:, stationary_index]
        stationary_distribution /= np.sum(stationary_distribution)

        return stationary_distribution
    
props = ['p', 'q', 'r']
I = BeliefBase(props, [['iff', 'r', 'implies', 'p', 'q']])

J1 = AgentFromModels((1, 0, 0), 'A')
J2 = AgentFromModels((1, 1, 1), 'B')
J3 = AgentFromModels((0, 0, 1), 'C')

G = GraphFromModels(I.models, [J1, J2, J3])

G.add_connections(J1, [J1, J2, J3])
G.add_connections(J2, [J1, J2])
G.add_connections(J3, [J3])

MC = MarkovChain(G)