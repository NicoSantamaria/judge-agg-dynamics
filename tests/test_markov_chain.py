import pytest
import numpy as np
from typing import List
from src.Graph import Graph
from src.BeliefBase import BeliefBase
from src.MarkovChain import MarkovChain
from utils.enums import Z2, Prop, Logic
from utils.types import Connection, Interpretation

def test_markov_chain_init():
    models: List[Interpretation] = [[Z2(1), Z2(0)], [Z2(0), Z2(1)]]
    connections: List[Connection] = []
    agents: List[Interpretation] = []
    G = Graph(models, connections, agents)
    M = MarkovChain(G)
    assert M.agents == []
    assert np.array_equal(M.model_matrix, np.array([
        [1, 0],
        [0, 1]
    ]))
    assert np.array_equal(M.coord_matrix, np.array([]))

    models: List[Interpretation] = [[Z2(1), Z2(0)], [Z2(0), Z2(1)]]
    connections: List[Connection] = [(models[0], models[1])]
    agents: List[Interpretation] = [models[0], models[1]]
    G = Graph(models, connections, agents)
    M = MarkovChain(G)
    assert M.agents == [[1, 0], [0, 1]]
    assert np.array_equal(M.model_matrix, np.array([
        [1, 0],
        [0, 1]
    ]))
    assert np.array_equal(M.coord_matrix, np.array([
        [1, 0],
        [0, 1]
    ]))

    K = BeliefBase([Prop.P, Prop.Q], [[Logic.AND, Prop.P, Prop.Q], [Logic.NOT, Prop.Q]])
    connections: List[Connection] = []
    agents: List[Interpretation] = []
    G = Graph(K, connections, agents)
    M = MarkovChain(G)
    assert M.agents == []
    assert np.array_equal(M.model_matrix, np.array([]))
    assert np.array_equal(M.coord_matrix, np.array([]))

    K = BeliefBase([Prop.P, Prop.Q, Prop.R], [[Logic.IFF, Prop.R, Logic.IMPLIES, Prop.P, Prop.Q]])
    connections: List[Connection] = [(K.models[0], K.models[1]), (K.models[0], K.models[2])]
    agents: List[Interpretation] = [K.models[0], K.models[1], K.models[2]]
    G = Graph(K, connections, agents)
    M = MarkovChain(G)
    print(M.agents)
    assert M.agents == [[0, 0, 1], [0, 1, 1], [1, 0, 0]]
    assert np.array_equal(M.model_matrix, np.array([
        [0, 0, 1, 1],
        [0, 1, 0, 1],
        [1, 1, 0, 1],
    ]))
    assert np.array_equal(M.coord_matrix, np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
        [0, 0, 0],
    ]))
