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

    def generate_states() -> StateGraph:
        return
    
    def fast_exponent(mat: Matrix) -> Matrix:
        eigenvalues, eigenvectors = np.linalg.eig(mat)
        diagonal = np.diag(eigenvalues)
        trans_matrix_inv = np.linalg.inv(eigenvectors)

        return reduce(np.matmul, [
            eigenvectors, 
            np.linalg.matrix_power(diagonal, 1000), 
            trans_matrix_inv
        ])

    def find_stationary(mat: Matrix) -> Matrix:
        eigenvalues, eigenvectors = np.linalg.eig(mat)
        stationary_index = np.where(np.isclose(eigenvalues, 1))[0][0]
        stationary_distribution = eigenvectors[:, stationary_index]
        stationary_distribution /= np.sum(stationary_distribution)

        return stationary_distribution