import numpy as np
from itertools import product, permutations
from functools import reduce
from Graph import *
from typing import *
from AgentFromModels import *
from GraphFromModels import *
from copy import deepcopy

type Matrix = np.ndarray
type StateGraph = Dict[GraphFromModels, List[Connection]]
type State = List[Tuple[str, Interpretation]]

class MarkovChain:
    def __init__(self, graph: GraphFromModels):
        self.graph: GraphFromModels = graph
        self.states: List[State] = self.generate_states()
        self.state_graph: StateGraph = self.build_state_graph()

    def generate_states(self) -> List[State]:
        # number of states can be easliy computed beforehand, so this can
        # be improved by initializing the list and avoiding the append
        # later on
        states: List[GraphFromModels] = list()
        
        models_combos = product(self.graph.models, repeat=len(self.graph.graph))
        agents_perms = permutations(self.graph.graph)
        
        for agents, models in product(agents_perms, models_combos):
            new_state: State = [(agent.name, model) for agent, model in zip(agents, models)]
            states.append(new_state)

        return states
    
    def build_state_graph(self) -> StateGraph:
        state_graph = dict()
        """
        How this will work:

        First, construct a copy of the original graph. Use
        the copy for the next operations

        For each state in self.states:
            1. update all of the agents in the graph to the 
            the beliefs in the state
            2. call the update rule, producing all the best
            tied outcomes
        
        Need to think about a good data structure to store all 
        the information, and an efficient way to compute
        """
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
    
# props = ['p', 'q', 'r']
# I = BeliefBase(props, [['iff', 'r', 'implies', 'p', 'q']])

# J1 = AgentFromModels((1, 0, 0), 'A')
# J2 = AgentFromModels((1, 1, 1), 'B')
# J3 = AgentFromModels((0, 0, 1), 'C')

# G = GraphFromModels(I.models, [J1, J2, J3])

# G.add_connections(J1, [J1, J2, J3])
# G.add_connections(J2, [J1, J2])
# G.add_connections(J3, [J3])

# MC = MarkovChain(G)