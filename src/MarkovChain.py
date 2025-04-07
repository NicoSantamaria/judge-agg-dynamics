import numpy as np
from itertools import product
from typing import List, Tuple, cast
from utils.types import Interpretation, Matrix, MatrixZ2
from utils.enums import Z2
from utils.utils import (hamming_distance, matrix_z2_to_matrix,
                         matrix_to_matrix_z2, find_stationary)
from src.Graph import Graph


# TODO: For experiments, add method to get frequency of all possible end states
# TODO: get result by state
# TODO: test get_state_models and get_result_by_state
# TODO: Pretty printing and by_agent option for get_result_by_state
# TODO: Do not build states, state_graph_matrix and stationary until necessary
# TODO: function to get result for single iteration of distance rule?
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

        # we probably don't want to have to call states of state_graph_matrix until
        # necessary for performance reasons, since those are the most expensive
        # operations
        self.states: List[MatrixZ2] = self._get_possible_states(
            np.full(self.coord_matrix.shape, Z2.ONE, dtype=object)
        )
        self.state_graph_matrix: Matrix = self._build_state_graph()
        self.stationary: Matrix = find_stationary(self.state_graph_matrix)

    # needs testing
    def get_state_models(self, coord_matrix: MatrixZ2 | None=None) -> MatrixZ2:
        if coord_matrix is None:
            coord_matrix = self.coord_matrix

        if self.model_matrix.shape == 0 == coord_matrix.shape:
            return np.array([])
        elif self.model_matrix.shape[1] != coord_matrix.shape[0]:
            raise ValueError("Model and coord matrices must be compatible for matrix multiplication.")
        return np.matmul(self.model_matrix, coord_matrix)


    def get_result_by_state(self, coord_matrix: MatrixZ2 | None=None) -> List[Tuple[float, MatrixZ2]]:
        if coord_matrix is None:
            coord_matrix = self.coord_matrix

        results: List[Tuple[float, MatrixZ2]] = []
        for i, state in enumerate(self.states):
            if np.array_equal(coord_matrix, state):
                end_state_probs = self.stationary[i]
                for end_state_index, end_state_prob in enumerate(end_state_probs):
                    end_state_prob = cast(float, end_state_prob)
                    if end_state_prob != 0:
                        results.append((
                            end_state_prob,
                            self.get_state_models(self.states[end_state_index])
                        ))
        return results


    @staticmethod
    def model_distances(mat1: MatrixZ2, mat2: MatrixZ2) -> Matrix:
        if mat1.size == 0 or mat2.size == 0:
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


    def update_from_state(self, coord_matrix: MatrixZ2) -> MatrixZ2:
        if coord_matrix.size == 0 == self.coord_matrix.size:
            return np.array([])
        elif coord_matrix.shape != self.coord_matrix.shape:
            raise ValueError("Coordinate matrices must have same dimensions.")

        distances: Matrix = np.matmul(
            self.model_distances(
                np.transpose(self.model_matrix),
                np.matmul(self.model_matrix, coord_matrix)
            ),
            matrix_z2_to_matrix(np.transpose(self.adjacency))
        )

        min_vals = np.min(distances, axis=0)
        next_coord_matrix = np.zeros_like(distances)
        for col in range(distances.shape[1]):
            min_mask = (distances[:, col] == min_vals[col])
            next_coord_matrix[:, col] = min_mask.astype(int)

        return matrix_to_matrix_z2(next_coord_matrix)


    def _get_possible_states(self, next_coord_matrix: MatrixZ2) -> List[MatrixZ2]:
        if next_coord_matrix.size == 0 == self.coord_matrix.size:
            return []
        if next_coord_matrix.shape != self.coord_matrix.shape:
            raise ValueError("Coordinate matrices must have same dimensions.")

        coord_matrix: Matrix = matrix_z2_to_matrix(next_coord_matrix)
        ones_positions: List[Matrix] = []
        for col in range(coord_matrix.shape[1]):
            rows_with_ones: Matrix = np.where(coord_matrix[:, col] == 1.)[0]
            ones_positions.append(rows_with_ones)

        valid_arrays: List[MatrixZ2] = []
        for combo in product(*ones_positions):
            new_arr = np.zeros_like(coord_matrix)
            for col, row in enumerate(combo):
                new_arr[row, col] = 1.
            valid_arrays.append(matrix_to_matrix_z2(new_arr))

        return valid_arrays


    def _build_state_graph(self) -> Matrix:
        dim: int = len(self.states)
        state_graph_matrix: Matrix = np.zeros((dim, dim))
        for i, state in enumerate(self.states):
            next_states: List[MatrixZ2] = self._get_possible_states(
                self.update_from_state(state)
            )

            for j in range(dim):
                for next_state in next_states:
                    if np.array_equal(self.states[j], next_state):
                        state_graph_matrix[i, j] = 1 / len(next_states)

        return state_graph_matrix

