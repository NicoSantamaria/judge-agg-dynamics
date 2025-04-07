import pytest
from typing import List
from src.Graph import Graph
from src.BeliefBase import BeliefBase
from utils.enums import Z2, Prop, Logic
from utils.types import Connection, Interpretation


# should use the test case from test_markov_chain where two agentshave the same model
def test_graph_init():
    models: List[Interpretation] = [[Z2(1), Z2(0)], [Z2(0), Z2(1)]]
    connections: List[Connection] = []
    agents: List[Interpretation] = []
    G = Graph(models, connections, agents)
    assert G.models == models

    models: List[Interpretation] = [[Z2(1), Z2(0)], [Z2(0), Z2(1)]]
    connections: List[Connection] = [(0, 1)]
    agents: List[Interpretation] = [models[0], models[1]]
    G = Graph(models, connections, agents)
    assert G.models == models

    models: List[Interpretation] = []
    connections: List[Connection] = []
    agents: List[Interpretation] = []
    G = Graph(models, connections, agents)
    assert G.models == models

    K = BeliefBase([Prop.P, Prop.Q], [])
    connections: List[Connection] = []
    agents: List[Interpretation] = []
    G = Graph(K, connections, agents)
    assert G.models == K.models

    K = BeliefBase([Prop.P, Prop.Q], [])
    connections: List[Connection] = [(0, 0)]
    agents: List[Interpretation] = [K.models[0]]
    G = Graph(K, connections, agents)
    assert G.models == K.models

    K = BeliefBase([Prop.P, Prop.Q], [[Logic.AND, Prop.P, Prop.Q], [Logic.NOT, Prop.Q]])
    connections: List[Connection] = []
    agents: List[Interpretation] = []
    G = Graph(K, connections, agents)
    assert G.models == K.models

    K = BeliefBase([Prop.P, Prop.Q, Prop.R], [[Logic.IFF, Prop.R, Logic.IMPLIES, Prop.P, Prop.Q]])
    connections: List[Connection] = [(0, 1), (0, 2)]
    agents: List[Interpretation] = [K.models[0], K.models[1], K.models[2]]
    G = Graph(K, connections, agents)
    assert G.models == K.models

    models: List[Interpretation] = []
    connections: List[Connection] = [(0, 1)]
    agents: List[Interpretation] = []
    with pytest.raises(ValueError, match="Connections can only be drawn between agents."):
        G = Graph(models, connections, agents)

    models: List[Interpretation] = [[Z2(1), Z2(0)], [Z2(0), Z2(1)]]
    connections: List[Connection] = [(0, 2)]
    agents: List[Interpretation] = [[Z2(1), Z2(0)], [Z2(0), Z2(1)]]
    with pytest.raises(ValueError, match="Connections can only be drawn between agents."):
        G = Graph(models, connections, agents)

    models: List[Interpretation] = [[Z2(1), Z2(0)], [Z2(0), Z2(1)]]
    connections: List[Connection] = []
    agents: List[Interpretation] = [[Z2(0), Z2(0)]]
    with pytest.raises(ValueError, match="Agents must be represented by models."):
        G = Graph(models, connections, agents)

    models: List[Interpretation] = [[Z2(1), Z2(0)], [Z2(0), Z2(1)]]
    connections: List[Connection] = [(0, 1)]
    agents: List[Interpretation] = []
    with pytest.raises(ValueError, match="Connections can only be drawn between agents."):
        G = Graph(models, connections, agents)

    K = BeliefBase([Prop.P, Prop.Q, Prop.R], [[Logic.IFF, Prop.R, Logic.IMPLIES, Prop.P, Prop.Q]])
    connections: List[Connection] = [(1, 1)]
    agents: List[Interpretation] = [[Z2(1), Z2(1), Z2(1)], [Z2(1), Z2(0), Z2(1)]]
    with pytest.raises(ValueError, match="Agents must be represented by models."):
        G = Graph(K, connections, agents)

    K = BeliefBase([Prop.P, Prop.Q, Prop.R], [[Logic.IFF, Prop.R, Logic.IMPLIES, Prop.P, Prop.Q]])
    connections: List[Connection] = [(1, 2)]
    agents: List[Interpretation] = []
    with pytest.raises(ValueError, match="Connections can only be drawn between agents."):
        G = Graph(K, connections, agents)

def test_add_connection():
    models: List[Interpretation] = [[Z2(1), Z2(0)], [Z2(0), Z2(1)]]
    connections: List[Connection] = [(0, 1)]
    agents: List[Interpretation] = [models[0], models[1]]
    G = Graph(models, connections, agents)
    G.add_connection((1, 1))
    assert G.connections == [(0, 1), (1, 1)]

    K = BeliefBase([Prop.P, Prop.Q], [])
    connections: List[Connection] = [(0, 0)]
    agents: List[Interpretation] = [K.models[0], K.models[1]]
    G = Graph(K, connections, agents)
    G.add_connection((1, 1))
    assert G.connections == [(0, 0), (1, 1)]

    K = BeliefBase([Prop.P, Prop.Q, Prop.R], [[Logic.IFF, Prop.R, Logic.IMPLIES, Prop.P, Prop.Q]])
    connections: List[Connection] = [(0, 1), (0, 2)]
    agents: List[Interpretation] = [K.models[0], K.models[1], K.models[2]]
    G = Graph(K, connections, agents)
    G.add_connection((1, 1))
    assert G.connections == [(0, 1), (0, 2), (1, 1)]

    K = BeliefBase([Prop.P, Prop.Q], [[Logic.AND, Prop.P, Prop.Q], [Logic.NOT, Prop.Q]])
    connections: List[Connection] = []
    agents: List[Interpretation] = []
    G = Graph(K, connections, agents)
    with pytest.raises(ValueError, match="Connections can only be drawn between agents."):
        G.add_connection((0, 1))


def test_remove_connection():
    models: List[Interpretation] = [[Z2(1), Z2(0)], [Z2(0), Z2(1)]]
    connections: List[Connection] = [(0, 1)]
    agents: List[Interpretation] = [models[0], models[1]]
    G = Graph(models, connections, agents)
    G.remove_connection((0, 1))
    assert G.connections == []

    K = BeliefBase([Prop.P, Prop.Q], [])
    connections: List[Connection] = [(0, 0)]
    agents: List[Interpretation] = [K.models[0], K.models[1]]
    G = Graph(K, connections, agents)
    G.remove_connection((0, 0))
    assert G.connections == []

    K = BeliefBase([Prop.P, Prop.Q, Prop.R], [[Logic.IFF, Prop.R, Logic.IMPLIES, Prop.P, Prop.Q]])
    connections: List[Connection] = [(0, 1), (0, 2)]
    agents: List[Interpretation] = [K.models[0], K.models[1], K.models[2]]
    G = Graph(K, connections, agents)
    G.remove_connection((0, 1))
    assert G.connections == [(0, 2)]

    K = BeliefBase([Prop.P, Prop.Q], [[Logic.AND, Prop.P, Prop.Q], [Logic.NOT, Prop.Q]])
    connections: List[Connection] = []
    agents: List[Interpretation] = []
    G = Graph(K, connections, agents)
    with pytest.raises(ValueError, match="Connection to be removed was not found."):
        G.remove_connection((0, 2))

def test_complete_graph():
    models: List[Interpretation] = [[Z2(0)]]
    connections: List[Connection] = []
    agents: List[Interpretation] = [models[0]]
    G = Graph(models, connections, agents)
    G.complete_graph()
    assert G.connections == [(0, 0)]

    K = BeliefBase([Prop.P, Prop.Q], [])
    connections: List[Connection] = [(0, 0)]
    agents: List[Interpretation] = [K.models[0], K.models[1]]
    G = Graph(K, connections, agents)
    G.complete_graph()
    assert G.connections == [(0, 0), (0, 1), (1, 0), (1, 1)]

def test_hamming_distance_rule():
    K = BeliefBase([Prop.P], [])
    agents: List[Interpretation] = [[Z2(0)], [Z2(1)]]
    connections: List[Connection] = [(0, 0), (0, 1), (1, 1)]
    G = Graph(K, connections, agents)
    assert G.hamming_distance_rule(0) == [agents[0], agents[1]]

    K = BeliefBase([Prop.P], [])
    agents: List[Interpretation] = [[Z2(0)], [Z2(1)]]
    connections: List[Connection] = [(0, 0), (0, 1), (1, 1)]
    G = Graph(K, connections, agents)
    assert G.hamming_distance_rule(1) == [agents[1]]

    K = BeliefBase([Prop.P, Prop.Q, Prop.R], [[Logic.IFF, Prop.R, Logic.IMPLIES, Prop.P, Prop.Q]])
    connections: List[Connection] = []
    agents: List[Interpretation] = [[Z2(1), Z2(0), Z2(0)], [Z2(0), Z2(0), Z2(1)], [Z2(1), Z2(1), Z2(1)]]
    G = Graph(K, connections, agents)
    G.complete_graph()
    assert G.hamming_distance_rule(0) ==  [
        [Z2(0), Z2(0), Z2(1)],
        [Z2(1), Z2(0), Z2(0)],
        [Z2(1), Z2(1), Z2(1)]
    ]
    assert G.hamming_distance_rule(2) ==  [
        [Z2(0), Z2(0), Z2(1)],
        [Z2(1), Z2(0), Z2(0)],
        [Z2(1), Z2(1), Z2(1)]
    ]

    K = BeliefBase([Prop.P], [])
    agents: List[Interpretation] = [[Z2(0)]]
    connections: List[Connection] = []
    G = Graph(K, connections, agents)
    with pytest.raises(ValueError, match="Agent not found in graph."):
        G.hamming_distance_rule(2)

def test_update():
    for _ in range(10):
        K = BeliefBase([Prop.P], [])
        agents: List[Interpretation] = [[Z2(0)], [Z2(1)]]
        connections: List[Connection] = [(0, 0), (0, 1), (1, 1)]
        G = Graph(K, connections, agents)
        G.update()
        assert G.agents[0] in [agents[0], agents[1]]
        assert G.agents[1] == agents[1]

        K = BeliefBase([Prop.P, Prop.Q, Prop.R], [[Logic.IFF, Prop.R, Logic.IMPLIES, Prop.P, Prop.Q]])
        connections: List[Connection] = []
        agents: List[Interpretation] = [[Z2(1), Z2(0), Z2(0)], [Z2(0), Z2(0), Z2(1)], [Z2(1), Z2(1), Z2(1)]]
        G = Graph(K, connections, agents)
        G.complete_graph()
        G.update()
        for agent in G.agents:
            assert agent in [[Z2(1), Z2(0), Z2(0)], [Z2(0), Z2(0), Z2(1)], [Z2(1), Z2(1), Z2(1)]]
