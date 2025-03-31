import pytest
from typing import List
from src.Graph import Graph
from src.BeliefBase import BeliefBase
from utils.enums import Z2, Prop, Logic
from utils.types import Connection, Interpretation


def test_init():
    models: List[Interpretation] = [[Z2(1), Z2(0)], [Z2(0), Z2(1)]]
    connections: List[Connection] = []
    agents: List[Interpretation] = []
    G = Graph(models, connections, agents)
    assert G.models == models

    models: List[Interpretation] = [[Z2(1), Z2(0)], [Z2(0), Z2(1)]]
    connections: List[Connection] = [(models[0], models[1])]
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
    connections: List[Connection] = [(K.models[0], K.models[0])]
    agents: List[Interpretation] = [K.models[0]]
    G = Graph(K, connections, agents)
    assert G.models == K.models

    K = BeliefBase([Prop.P, Prop.Q], [[Logic.AND, Prop.P, Prop.Q], [Logic.NOT, Prop.Q]])
    connections: List[Connection] = []
    agents: List[Interpretation] = []
    G = Graph(K, connections, agents)
    assert G.models == K.models

    K = BeliefBase([Prop.P, Prop.Q, Prop.R], [[Logic.IFF, Prop.R, Logic.IMPLIES, Prop.P, Prop.Q]])
    connections: List[Connection] = [(K.models[0], K.models[1]), (K.models[0], K.models[2])]
    agents: List[Interpretation] = [K.models[0], K.models[1], K.models[2]]
    G = Graph(K, connections, agents)
    assert G.models == K.models

    # models: List[Interpretation] = []
    # connections: List[Connection] = [([Z2(0)], [Z2(1)])]
    # with pytest.raises(ValueError, match="Connections can only be drawn between models."):
    #     G = Graph(models, connections)

    # models: List[Interpretation] = [[Z2(1), Z2(0)], [Z2(0), Z2(1)]]
    # connections: List[Connection] = [([Z2(0)], [Z2(1)])]
    # with pytest.raises(ValueError, match="Connections can only be drawn between models."):
    #     G = Graph(models, connections)

    # models: List[Interpretation] = [[Z2(1), Z2(0)], [Z2(0), Z2(1)]]
    # connections: List[Connection] = [([Z2(0), Z2(0)], [Z2(1), Z2(0)])]
    # with pytest.raises(ValueError, match="Connections can only be drawn between models."):
    #     G = Graph(models, connections)

    # models: List[Interpretation] = [[Z2(1), Z2(0)], [Z2(0), Z2(1)]]
    # connections: List[Connection] = [([Z2(1), Z2(0)], [Z2(1), Z2(1)])]
    # with pytest.raises(ValueError, match="Connections can only be drawn between models."):
    #     G = Graph(models, connections)

    # K = BeliefBase([Prop.P, Prop.Q, Prop.R], [[Logic.IFF, Prop.R, Logic.IMPLIES, Prop.P, Prop.Q]])
    # connections: List[Connection] = [([Z2(1), Z2(0), Z2(1)], [Z2(1), Z2(1), Z2(1)])]
    # with pytest.raises(ValueError, match="Connections can only be drawn between models."):
    #     G = Graph(K, connections)

# test add_connection, remove_connection, complete_graph
