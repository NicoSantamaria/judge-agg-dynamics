import numpy as np
from itertools import product
from typing import List
from AgentFromModels import AgentFromModels
from GraphFromModels import GraphFromModels



class MarkovChain:
    def __init__(self, graph: GraphFromModels):
        self.agents: List[AgentFromModels] = list(graph.graph)
        self.model_matrix: Matrix = np.matrix_transpose(graph.models)

        self.coord_matrix: Matrix = self._get_coord_matrix(self.agents, self.model_matrix)
        self.adjacency = self._get_adjacency_matrix(self.agents, graph)
        self.states: List[Matrix] = self._get_possible_states(np.ones(self.coord_matrix.shape))
        self.state_graph_matrix: Matrix = self._build_state_graph()
        self.stationary: Matrix = self.find_stationary(self.state_graph_matrix)


    @staticmethod
    def _get_coord_matrix(agents: List[AgentFromModels], model_matrix: Matrix) -> Matrix:
        rows: int = len(model_matrix[0])
        cols: int = len(agents)
        coord_matrix: Matrix = np.zeros((rows, cols))

        for i, agent in enumerate(agents):
            for j, model in enumerate(np.transpose(model_matrix)):
                if agent.model == tuple(model):
                    coord_matrix[j, i] = 1

        return coord_matrix


    @staticmethod
    def _get_adjacency_matrix(agents: List[AgentFromModels], graph: GraphFromModels) -> Matrix:
        dim: int = len(agents)
        adjacency: Matrix = np.zeros((dim, dim))

        for i in range(dim):
            for j in range(dim):
                agent = agents[i]
                connection = agents[j]

                if connection in graph.graph[agent]:
                    adjacency[i, j] = 1

        return adjacency


    @staticmethod
    def model_distances(mat1: Matrix, mat2: Matrix) -> Matrix:
        rows: int = mat1.shape[0]
        cols: int = mat2.shape[1]
        distance_matrix: Matrix = np.zeros((rows, cols))

        for i, model1 in enumerate(mat1):
            for j, model2 in enumerate(np.transpose(mat2)):
                distance: int = 0

                # replace with utils hamming_distance
                for pos1, pos2 in zip(tuple(model1), tuple(model2)):
                    if pos1 != pos2:
                        distance += 1

                distance_matrix[i, j] = distance

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
