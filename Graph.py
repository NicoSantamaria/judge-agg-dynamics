from Agent import *
from BeliefBase import *
from typing import *
import random

type Connection = List[Tuple[int, Agent]]
type GraphEdges = Dict[Agent, List[Connection]]

class Graph:
    def __init__(self, agenda: BeliefBase, agents: list[Agent]=list()) -> None:
        self.agenda: BeliefBase = agenda
        self.graph: GraphEdges = {agent: [agent] for agent in agents}

    def add_connections(self, agent: Agent, connections: list[Connection]) -> None:
        self.graph[agent] = connections 

    def tiebreaker_chance(self, interps: List[Interpretation]) -> Interpretation:
        return random.choice(interps)
    
    def hamming_distance(self, x: Interpretation, y: Interpretation) -> int:
        count: int = 0

        for a, b in zip(x, y):
            if a != b:
                count += 1

        return count

    
    # def hamming_distance_rule(self, agent: Agent) -> List[Interpretation]:
    #     candidates: List[Interpretation] = list()

    #     for model in self.agenda.models:
    #         for connection in self.graph[agent]:
    #             break

    #     return candidates


# testing
IC = BeliefBase(["p", "q", "r", "s"], [["iff", "r", "and", "p", "q"], ['iff', 's', 'not', 'or', 'p', 'r']])
K1 = Agent(IC, {"p": 0, "q": 0, "r": 0, "s": 1})
K2 = Agent(IC, {"p": 0, "q": 1, "r": 0, "s": 1})
G = Graph(IC, [K1, K2])
G.add_connections(K1, [K2])

# for connection in G.graph[K1]:
#     print(connection)