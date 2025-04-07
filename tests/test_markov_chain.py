import pytest
import numpy as np
from typing import List
from src.Graph import Graph
from src.BeliefBase import BeliefBase
from src.MarkovChain import MarkovChain
from utils.enums import Z2, Prop, Logic
from utils.types import Connection, Interpretation, MatrixZ2

def test_markov_chain_init():
    models: List[Interpretation] = [[Z2(1), Z2(0)], [Z2(0), Z2(1)]]
    connections: List[Connection] = []
    agents: List[Interpretation] = []
    G = Graph(models, connections, agents)
    M = MarkovChain(G)
    assert M.agents == []
    assert np.array_equal(M.model_matrix, np.array([
        [Z2(1), Z2(0)],
        [Z2(0), Z2(1)]
    ]))
    assert np.array_equal(M.coord_matrix, np.array([]))
    assert np.array_equal(M.adjacency, np.array([]))

    models: List[Interpretation] = [[Z2(1), Z2(0)], [Z2(0), Z2(1)]]
    connections: List[Connection] = [(0, 1)]
    agents: List[Interpretation] = [models[0], models[1]]
    G = Graph(models, connections, agents)
    M = MarkovChain(G)
    assert M.agents == [[Z2(1), Z2(0)], [Z2(0), Z2(1)]]
    assert np.array_equal(M.model_matrix, np.array([
        [Z2(1), Z2(0)],
        [Z2(0), Z2(1)]
    ]))
    assert np.array_equal(M.coord_matrix, np.array([
        [Z2(1), Z2(0)],
        [Z2(0), Z2(1)]
    ]))
    assert np.array_equal(M.adjacency, np.array([
        [Z2(0), Z2(1)],
        [Z2(0), Z2(0)]
    ]))

    K = BeliefBase([Prop.P, Prop.Q], [[Logic.AND, Prop.P, Prop.Q], [Logic.NOT, Prop.Q]])
    connections: List[Connection] = []
    agents: List[Interpretation] = []
    G = Graph(K, connections, agents)
    M = MarkovChain(G)
    assert M.agents == []
    assert np.array_equal(M.model_matrix, np.array([]))
    assert np.array_equal(M.coord_matrix, np.array([]))
    assert np.array_equal(M.adjacency, np.array([]))

    K = BeliefBase([Prop.P, Prop.Q, Prop.R], [[Logic.IFF, Prop.R, Logic.IMPLIES, Prop.P, Prop.Q]])
    connections: List[Connection] = [(0, 1), (0, 2)]
    agents: List[Interpretation] = [K.models[0], K.models[1], K.models[2]]
    G = Graph(K, connections, agents)
    M = MarkovChain(G)
    print(M.agents)
    assert M.agents == [[Z2(0), Z2(0), Z2(1)], [Z2(0), Z2(1), Z2(1)], [Z2(1), Z2(0), Z2(0)]]
    assert np.array_equal(M.model_matrix, np.array([
        [Z2(0), Z2(0), Z2(1), Z2(1)],
        [Z2(0), Z2(1), Z2(0), Z2(1)],
        [Z2(1), Z2(1), Z2(0), Z2(1)],
    ]))
    assert np.array_equal(M.coord_matrix, np.array([
        [Z2(1), Z2(0), Z2(0)],
        [Z2(0), Z2(1), Z2(0)],
        [Z2(0), Z2(0), Z2(1)],
        [Z2(0), Z2(0), Z2(0)],
    ]))
    assert np.array_equal(M.adjacency, np.array([
        [Z2(0), Z2(1), Z2(1)],
        [Z2(0), Z2(0), Z2(0)],
        [Z2(0), Z2(0), Z2(0)]
    ]))

    models: List[Interpretation] = [[Z2(1), Z2(1), Z2(1)], [Z2(0), Z2(0), Z2(0)], [Z2(1), Z2(0), Z2(1)]]
    connections: List[Connection] = [(0, 1), (0, 2), (1, 2), (2, 1), (3, 3), (3, 0), (3, 1)]
    agents: List[Interpretation] = [models[0], models[1], models[1], models[2]]
    G = Graph(models, connections, agents)
    M = MarkovChain(G)
    assert M.agents == [[Z2(1), Z2(1), Z2(1)], [Z2(0), Z2(0), Z2(0)], [Z2(0), Z2(0), Z2(0)], [Z2(1), Z2(0), Z2(1)]]
    assert np.array_equal(M.model_matrix, np.array([
        [Z2(1), Z2(0), Z2(1)],
        [Z2(1), Z2(0), Z2(0)],
        [Z2(1), Z2(0), Z2(1)]
    ]))
    assert np.array_equal(M.coord_matrix, np.array([
        [Z2(1), Z2(0), Z2(0), Z2(0)],
        [Z2(0), Z2(1), Z2(1), Z2(0)],
        [Z2(0), Z2(0), Z2(0), Z2(1)],
    ]))
    assert np.array_equal(M.adjacency, np.array([
        [Z2(0), Z2(1), Z2(1), Z2(0)],
        [Z2(0), Z2(0), Z2(1), Z2(0)],
        [Z2(0), Z2(1), Z2(0), Z2(0)],
        [Z2(1), Z2(1), Z2(0), Z2(1)]
    ]))

def test_model_matrix():
    M = MarkovChain(Graph([], [], []))

    A: MatrixZ2 = np.array([], dtype=object)
    B: MatrixZ2 = np.array([], dtype=object)
    assert np.array_equal(M.model_distances(A, B), np.array([]))

    A: MatrixZ2 = np.array([[Z2(1)]], dtype=object)
    B: MatrixZ2 = np.array([[Z2(1)]], dtype=object)
    assert np.array_equal(M.model_distances(A, B), np.array([[0]]))

    A: MatrixZ2 = np.array([[Z2(1)]], dtype=object)
    B: MatrixZ2 = np.array([[Z2(0)]], dtype=object)
    assert np.array_equal(M.model_distances(A, B), np.array([[1]]))

    A: MatrixZ2 = np.array([
        [Z2(1), Z2(0)],
        [Z2(1), Z2(0)]
    ], dtype=object)
    B: MatrixZ2 = np.array([
        [Z2(1), Z2(0)],
        [Z2(1), Z2(0)],
    ], dtype=object)
    assert np.array_equal(M.model_distances(A, B), np.array([
        [1, 1],
        [1, 1]
    ]))

    A: MatrixZ2 = np.array([
        [Z2(1), Z2(0), Z2(1)],
        [Z2(0), Z2(1), Z2(1)]
    ], dtype=object)
    B: MatrixZ2 = np.array([
        [Z2(0), Z2(0)],
        [Z2(1), Z2(0)],
        [Z2(0), Z2(1)],
    ], dtype=object)
    assert np.array_equal(M.model_distances(A, B), np.array([
        [3, 1],
        [1, 1],
    ]))

    A: MatrixZ2 = np.array([
        [Z2(0), Z2(0), Z2(1)],
        [Z2(1), Z2(0), Z2(0)],
        [Z2(0), Z2(1), Z2(1)],
        [Z2(1), Z2(1), Z2(1)],
    ], dtype=object)
    B: MatrixZ2 = np.array([
        [Z2(1), Z2(1), Z2(0)],
        [Z2(0), Z2(1), Z2(0)],
        [Z2(0), Z2(1), Z2(1)],
    ], dtype=object)
    assert np.array_equal(M.model_distances(A, B), np.array([
        [2, 2, 0],
        [0, 2, 2],
        [3, 1, 1],
        [2, 0, 2]
    ]))

    A: MatrixZ2 = np.array([
        [Z2(0), Z2(0), Z2(1)],
        [Z2(1), Z2(0), Z2(0)],
        [Z2(0), Z2(0), Z2(1)],
        [Z2(1), Z2(0), Z2(0)],
    ], dtype=object)
    B: MatrixZ2 = np.array([
        [Z2(1), Z2(1), Z2(0)],
        [Z2(0), Z2(1), Z2(0)],
    ], dtype=object)
    with pytest.raises(ValueError, match="Matrices must be compatible for multiplication to find model distances."):
        M.model_distances(A, B)

def test_update_from_state():
    M = MarkovChain(Graph([], [], []))
    assert np.array_equal(M.update_from_state(np.array([])), np.array([]))

    K = BeliefBase([Prop.P, Prop.Q, Prop.R], [[Logic.IFF, Prop.R, Logic.IMPLIES, Prop.P, Prop.Q]])
    G = Graph(K,
        [(0, 0), (0, 1), (0, 2), (1, 1), (1, 0), (2, 2)],
        [[Z2(1), Z2(0), Z2(0)], [Z2(1), Z2(1), Z2(1)], [Z2(0), Z2(0), Z2(1)]]
    )
    M = MarkovChain(G)
    print(M.coord_matrix)
    assert np.array_equal(
        M.update_from_state(M.coord_matrix),
        np.array([
            [Z2(1), Z2(0), Z2(1)],
            [Z2(0), Z2(0), Z2(0)],
            [Z2(1), Z2(1), Z2(0)],
            [Z2(1), Z2(1), Z2(0)],
        ])
    )

    with pytest.raises(ValueError, match="Coordinate matrices must have same dimensions."):
        M.update_from_state(np.array([
            [Z2(1), Z2(1)],
            [Z2(0), Z2(0)]
        ]))