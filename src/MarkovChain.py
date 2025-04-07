import numpy as np
from itertools import product
from typing import List, cast
from utils.types import Interpretation, Matrix, MatrixZ2
from utils.enums import Z2
from utils.utils import hamming_distance, ints_to_interpretation
from src.Graph import Graph


# TODO: For experiments, add method to get frequency of all possible end states
# given a starting state
# Could handle this more cleanly with multiple dispatching?
# TODO (immediately): translate and test update_from_state
class MarkovChain:
    def __init__(self, graph: Graph) -> None:
        self.agents: List[Interpretation] = graph.agents
        self.model_matrix: MatrixZ2 = np.transpose(np.array(graph.models))

        if self.model_matrix.size > 0 and len(self.agents) > 0:
            rows = len(self.model_matrix[0])
            cols = len(self.agents)
            self.coord_matrix: MatrixZ2 = np.empty((rows, cols), dtype=object)

            agent_tuples = [tuple(agent) for agent in self.agents]
            model_tuples = [tuple(model) for model in np.transpose(self.model_matrix)]

            for i, agent_tuple in enumerate(agent_tuples):
                for j, model_tuple in enumerate(model_tuples):
                    if agent_tuple == model_tuple:
                        self.coord_matrix[j, i] = Z2.ONE
                    else:
                        self.coord_matrix[j, i] = Z2.ZERO
        else:
            self.coord_matrix = np.array([])

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


        # self.states: List[Matrix] = self._get_possible_states(np.ones(self.coord_matrix.shape))
        # self.state_graph_matrix: Matrix = self._build_state_graph()
        # self.stationary: Matrix = self.find_stationary(self.state_graph_matrix)


    @staticmethod
    def model_distances(mat1: MatrixZ2, mat2: MatrixZ2) -> Matrix:
        if np.array_equal(mat1, np.array([])) or np.array_equal(mat2, np.array([])):
            return np.array([])

        mat1_rows, mat1_cols = mat1.shape
        mat2_rows, mat2_cols = mat2.shape
        distance_matrix: Matrix = np.zeros((mat1_rows, mat2_cols))

        if mat1_cols != mat2_rows:
            raise ValueError("Matrices must be compatible for multiplication to find model distances.")

        for i, model1 in enumerate(mat1):
            for j, model2 in enumerate(np.transpose(mat2)):
                model1 = cast(Interpretation, model1)
                model2 = cast(Interpretation, model2)
                distance_matrix[i, j] = hamming_distance(model1, model2)

        return distance_matrix


    def update_from_state(self, coord_matrix: Matrix) -> Matrix:
        distances: Matrix = np.matmul(
            self.model_distances(
                np.transpose(self.model_matrix),
                np.matmul(
                    self.model_matrix,
                    coord_matrix
                )
            ),
            np.transpose(self.adjacency)
        )

        # Find minimum value in each column
        min_vals = np.min(distances, axis=0)  # axis=0 means operate along columns

        # Create a new array with the same shape as the original
        # Fill with 1 where value equals the column minimum, 0 elsewhere
        next_coord_matrix = np.zeros_like(distances)

        # For each column
        for col in range(distances.shape[1]):
            # Create a boolean mask where the value equals the minimum for this column
            min_mask = (distances[:, col] == min_vals[col])
            # Set those positions to 1 in the result array
            next_coord_matrix[:, col] = min_mask.astype(int)

        return next_coord_matrix


    @staticmethod
    def _get_possible_states(next_coord_matrix: Matrix) -> List[Matrix]:
        # Get the positions where 1s are in the original array
        ones_positions = []
        for col in range(next_coord_matrix.shape[1]):
            # Get the row indices where there are 1s in this column
            rows_with_ones = np.where(next_coord_matrix[:, col] == 1.)[0]
            ones_positions.append(rows_with_ones)

        # Generate all combinations using the cartesian product
        valid_arrays = []
        for combo in product(*ones_positions):
            # Create a zero array of the same shape as original
            new_arr = np.zeros_like(next_coord_matrix)

            # Place 1s at the selected positions
            for col, row in enumerate(combo):
                new_arr[row, col] = 1.

            valid_arrays.append(new_arr)

        return valid_arrays


    def _build_state_graph(self) -> Matrix:
        dim: int = len(self.states)
        state_graph_matrix: Matrix = np.zeros((dim, dim))

        for i, state in enumerate(self.states):
            next_states = self._get_possible_states(
                self.update_from_state(state)
            )

            probability = 1 / len(next_states)

            for j in range(dim):
                for next_state in next_states:
                    if np.array_equal(self.states[j], next_state):
                        state_graph_matrix[i, j] = probability

        return state_graph_matrix


    def find_stationary(self, mat: Matrix) -> Matrix:
        stationary = np.linalg.matrix_power(mat, 1000)
        stationary = np.where(
            np.isclose(stationary, 0), 0, stationary
        )
        return stationary
