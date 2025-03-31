from typing import List
from src.Graph import Graph
from utils.enums import Z2
from utils.types import Connection, Interpretation


def test_init():
    models: List[Interpretation] = [[Z2(1), Z2(0)], [Z2(0), Z2(1)]]
    connections: List[Connection] = []
    G = Graph(models, connections)
    assert G.models == models

    models: List[Interpretation] = [[Z2(1), Z2(0)], [Z2(0), Z2(1)]]
    connections: List[Connection] = [(models[0], models[1])]
    G = Graph(models, connections)
    assert G.models == models

    models: List[Interpretation] = []
    connections: List[Connection] = []
    G = Graph(models, connections)
    assert G.models == models
