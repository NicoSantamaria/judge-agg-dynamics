import numpy as np
from functools import reduce
from Graph import *
from typing import *

type Matrix = np.ndarray
type StateGraph = Dict[Graph, List[Connection]]

class MarkovChain:
    def __init__(self, graph: Graph):
        self.graph: Graph = graph
        self.state_graph: StateGraph = self.generate_states()

    def generate_states(self) -> StateGraph:
        for agent in self.graph.graph:
            for model in self.graph.agenda.models:
                print(agent.name, model)

        return 
    
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
J1 = Agent(I, dict(zip(props, [0,0,1])), 'A')
J2 = Agent(I, dict(zip(props, [1,1,1])), 'B')
J3 = Agent(I, dict(zip(props, [0,0,1])), 'C')

G = Graph(I, [J1, J2, J3])
G.add_connections(J1, [J1, J2, J3])
G.add_connections(J2, [J1, J2])
G.add_connections(J3, [J3])

MC = MarkovChain(G)