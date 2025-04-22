import numpy as np
from itertools import product
from typing import List, Tuple, cast
from src.jaggdy.utils.types import Interpretation, Matrix, MatrixZ2
from src.jaggdy.utils.enums import Z2
from src.jaggdy.utils.utils import (hamming_distance, matrix_z2_to_matrix,
                         matrix_to_matrix_z2, find_stationary)
from src.jaggdy.Graph import Graph


# TODO: For experiments, add method to get frequency of all possible end states
# TODO: get result by state
# TODO: test get_state_models and get_result_by_state
# TODO: Pretty printing and by_agent option for get_result_by_state
# TODO: Do not build states, state_graph_matrix and stationary until necessary
# TODO: function to get result for single iteration of distance rule?
# TODO: Docstrings and comments
# TODO: Move stationary matrix method back to class, check eigenvalues
# TODO: Rice lecture notes as reference for stationary matrix
class MarkovChain:
    """
    From a Graph object, constructs every possible state that graph can
    assume and computes the probability of moving from each state to another
    after a single iteration of the Hamming distance-based aggregation rule. These
    probabilities form the entries of Markov transition matrix, which is used to
    compute a stationary matrix.

    ATTRIBUTES:
        agents (List[Interpretation]): The set of vectors representing rational agents.
        model_matrix (Matrix): A matrix with columns representing all the rational interpretations
        of the agenda with respect to the integrity constraints contained in the Graph object.
        coord_matrix (MatrixZ2): A matrix representing the coordinates of each agents' beliefs in
        the model_matrix.
        adjacency (MatrixZ2): Adjacency matrix for the Graph object-- each 1 entry at (i, j)
        represents a directed edge from agent i to agent j.
        states (List[MatrixZ2]): Every possible state the graph can take, as represented by coord
        matrices.
        state_graph_matrix (Matrix): The transition matrix for the Markov chain. Each entry (i, j)
        represents the probability of moving from state i to state j after a single iteration
        of the Hamming distance-based aggregation rule.
        self.stationary (Matrix): The stationary matrix for the Markov chain, computed from
        state_graph_matrix.


    REFERENCES:
        [1] Gabriella Pigozzi. Belief merging and the discursive dilemma: an
                argument-based account to paradoxes of judgment aggregation. Synthese,
                152(2):285–98, 2006.
        [2] Christian List. The theory of judgment aggregation: An introductory
                review. Synthese, 187(1):179–207, 2012.
        [3] Gregory Valiant and Mary Wootters. Lecture #13: introduction to markov chains, and a
                randomized algorithm for 2-SAT. 2025.
                https://web.stanford.edu/class/cs265/Lectures/Lecture13/l13.pdf

    """
    def __init__(self, graph: Graph) -> None:
        self.agents: List[Interpretation] = graph.agents
        self.model_matrix: MatrixZ2 = np.transpose(np.array(graph.models))

        # build coord_matrix from the agents and the model_matrix
        if self.model_matrix.size > 0 and len(self.agents) > 0:
            rows = len(self.model_matrix[0])
            cols = len(self.agents)
            self.coord_matrix: MatrixZ2 = np.empty((rows, cols), dtype=object)

            agent_tuples = [tuple(agent) for agent in self.agents]
            model_tuples = [tuple(model) for model in np.transpose(self.model_matrix)]

            # if the agent i's belief matches the j-th belief in the model matrix,
            # then coord_matrix[j, i] = 1, else 0.
            for i, agent_tuple in enumerate(agent_tuples):
                for j, model_tuple in enumerate(model_tuples):
                    if agent_tuple == model_tuple:
                        self.coord_matrix[j, i] = Z2.ONE
                    else:
                        self.coord_matrix[j, i] = Z2.ZERO
        else:
            self.coord_matrix: MatrixZ2 = np.array([], dtype=object)

        # build adjacency matrix
        dim: int = len(self.agents)
        if dim == 0:
            self.adjacency: MatrixZ2 = np.array([])
        else:
            self.adjacency: MatrixZ2 = np.empty((dim, dim), dtype=object)
            for (i, j) in product(range(dim), repeat=2):
                if (i, j) in graph.connections:
                    self.adjacency[i, j] = Z2.ONE
                else:
                    self.adjacency[i, j] = Z2.ZERO

        # build states, state_graph_matrix, and stationary
        # states is computed by finding all the permutations of matrices over
        # Z2 such that each column has exactly one 1; this is achieved by calling
        # get_possible states on a matrix of all 1s.
        self.states: List[MatrixZ2] = self._get_possible_states(
            np.full(self.coord_matrix.shape, Z2.ONE, dtype=object)
        )
        self.state_graph_matrix: Matrix = self._build_state_graph()
        self.stationary: Matrix = find_stationary(self.state_graph_matrix)


    def get_state_models(self, coord_matrix: MatrixZ2 | None=None) -> MatrixZ2:
        """
        From a given coordinate matrix, recover the models representing each agents' beliefs.

        :param coord_matrix: Matrix providing the coordinates of each agent's beliefs in model_matrix
        :return: Matrix where the j-th column represents the belief of the j-th agent.
        """
        if coord_matrix is None:
            coord_matrix = self.coord_matrix

        if self.model_matrix.shape == 0 == coord_matrix.shape:
            return np.array([])
        elif self.model_matrix.shape[1] != coord_matrix.shape[0]:
            raise ValueError("Model and coord matrices must be compatible for matrix multiplication.")

        # Models are recovered by multiplication of model and coord matrices.
        return np.matmul(self.model_matrix, coord_matrix)


    def get_result_by_state(self, coord_matrix: MatrixZ2 | None=None) -> List[Tuple[float, MatrixZ2]]:
        """
        For a given coord_matrix representing a state of the graph, returns the possible
        states that can be achieved after many iterations of the update rule together with
        the probability of attaining that state.

        :param coord_matrix: coord_matrix representing a possible initial graph state.
        :return: A list of probabilities of achieving each possible state, together with a matrix
        representing that state, where the j-th column represents the belief of agent j in
        that state.
        """
        if coord_matrix is None:
            coord_matrix = self.coord_matrix

        # Find all possible states together with their respective probabilities
        results: List[Tuple[float, MatrixZ2]] = []
        for i, state in enumerate(self.states):

            # Find the results from the stationary matrix for the given coord_matrix
            if np.array_equal(coord_matrix, state):
                end_state_probs = self.stationary[i]

                # Find all end states with non-zero probability from the initial
                for end_state_index, end_state_prob in enumerate(end_state_probs):
                    end_state_prob = cast(float, end_state_prob)

                    # append probability and possible state
                    if end_state_prob != 0:
                        results.append((
                            end_state_prob,
                            self.get_state_models(self.states[end_state_index])
                        ))

        return results


    @staticmethod
    def model_distances(mat1: MatrixZ2, mat2: MatrixZ2) -> Matrix:
        """
        Computes a matrix of distances between two matrices. Each (i, j) entry
        in the return matrix corresponds to the hamming distance between row i in
        mat1 and row j in mat2.

        :param mat1: A matrix over Z2.
        :param mat2: A matrix over Z2.
        :return: A matrix of hamming distances between rows in mat1 and columns in mat2.
        """
        if mat1.size == 0 or mat2.size == 0:
            return np.array([])

        # The computation technique mirrors matrix multiplication, so the matrices must be
        # compatible for matrix multiplication.
        mat1_rows, mat1_cols = mat1.shape
        mat2_rows, mat2_cols = mat2.shape
        distance_matrix: Matrix = np.zeros((mat1_rows, mat2_cols))
        if mat1_cols != mat2_rows:
            raise ValueError("Matrices must be compatible for multiplication to find model distances.")

        # entry (i, j) in the return matrix is the hamming_distance of row i in mat1
        # and column j in mat2.
        for i, model1 in enumerate(mat1):
            for j, model2 in enumerate(np.transpose(mat2)):
                model1 = cast(Interpretation, model1)
                model2 = cast(Interpretation, model2)
                distance_matrix[i, j] = hamming_distance(model1, model2)

        return distance_matrix


    def update_from_state(self, coord_matrix: MatrixZ2) -> MatrixZ2:
        """
        For a given coordinate matrix representing a state of the graph, returns a matrix
        where each entry (i, j) represents the possibility that agent j will adopt the
        i-th belief in the model matrix after a single iteration of the Hamming distance
        based aggregation rule.

        :param coord_matrix: A coordinate matrix over Z2 representing a possible graph state.
        :return: A matrix providing the coordinates of the possible judgments for each agent
        after a single iteration of the Hamming distance based aggregation rule on the coord_matrix.
        """
        if coord_matrix.size == 0 == self.coord_matrix.size:
            return np.array([])
        elif coord_matrix.shape != self.coord_matrix.shape:
            raise ValueError("Coordinate matrices must have same dimensions.")

        # Compute the distances from the agents' beliefs to every possible model.
        distances: Matrix = np.matmul(
            self.model_distances(
                np.transpose(self.model_matrix),
                np.matmul(self.model_matrix, coord_matrix)
            ),
            matrix_z2_to_matrix(np.transpose(self.adjacency))
        )

        # Find the minimum distances in each column and replace with 1; these are all
        # the distances that the agents in that column can possibly adopt
        min_vals = np.min(distances, axis=0)
        next_coord_matrix = np.zeros_like(distances)
        for col in range(distances.shape[1]):

            # Build a matrix indicating if each entry is minimal in its column.
            min_mask = (distances[:, col] == min_vals[col])
            next_coord_matrix[:, col] = min_mask.astype(int)

        return matrix_to_matrix_z2(next_coord_matrix)


    def _get_possible_states(self, next_coord_matrix: MatrixZ2) -> List[MatrixZ2]:
        """
        From a matrix providing the coordinates of the possible judgments for each agent
        after a single iteration of the Hamming distance based aggregation rule (such as that
        returned by the update_from_state method), returns a list of possible coordinate matrices
        where each agent adopts exactly one of those possible judgments. Amounts to finding all
        possible matrices with exactly one 1 entry in each column from a matrix over Z2.

        :param next_coord_matrix: A matrix providing the coordinates of the possible judgments
        for each agent after a single iteration of the Hamming distance based aggregation rule
        :return: All possible coordinate matrices where each agent adopts exactly one of
        those possible judgments after a single iteration of the Hamming distance based aggregation.
        """
        if next_coord_matrix.size == 0 == self.coord_matrix.size:
            return []
        if next_coord_matrix.shape != self.coord_matrix.shape:
            raise ValueError("Coordinate matrices must have same dimensions.")

        # Find the indices of all the rows with a 1 entry
        coord_matrix: Matrix = matrix_z2_to_matrix(next_coord_matrix)
        ones_positions: List[Matrix] = []
        for col in range(coord_matrix.shape[1]):
            rows_with_ones: Matrix = np.where(coord_matrix[:, col] == 1.)[0]
            ones_positions.append(rows_with_ones)

        # Find all permutations of rows with a 1 entry
        valid_arrays: List[MatrixZ2] = []
        for combo in product(*ones_positions):
            new_arr = np.zeros_like(coord_matrix)

            # From each permutation, construct the corresponding coord_matrix
            for col, row in enumerate(combo):
                new_arr[row, col] = 1.
            valid_arrays.append(matrix_to_matrix_z2(new_arr))

        return valid_arrays


    def _build_state_graph(self) -> Matrix:
        """
        Build the Markov transition matrix where each (i, j) entry
        represents the probability of attaining the state j from the
        state i.

        :return: The Markov transition matrix.
        """
        dim: int = len(self.states)
        state_graph_matrix: Matrix = np.zeros((dim, dim))
        for i, state in enumerate(self.states):

            # For each state, find all the possible next states
            next_states: List[MatrixZ2] = self._get_possible_states(
                self.update_from_state(state)
            )

            for j in range(dim):
                for next_state in next_states:

                    # Any of the possible next states can be attained with equal probability.
                    if np.array_equal(self.states[j], next_state):
                        state_graph_matrix[i, j] = 1 / len(next_states)

        return state_graph_matrix

