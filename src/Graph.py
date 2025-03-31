import random
from typing import List
from itertools import product
from utils.utils import hamming_distance
from utils.types import Interpretation, Connection
from src.BeliefBase import BeliefBase

# TODO: use networkx library to get graphics of each graph
# Potentially we also want to be able to input integers directly, like in beliefbase
class Graph:
    def __init__(self,
        models: List[Interpretation] | BeliefBase,
        connections: List[Connection],
        agents: List[Interpretation]=[]
    ) -> None:
        self.models: List[Interpretation] = []
        if isinstance(models, BeliefBase):
            self.models = models.models
        else:
            self.models = models

        for agent in agents:
            if agent not in self.models:
                raise ValueError("Agents must be represented by models.")
        self.agents = agents

        for model1, model2 in connections:
            if model1 not in self.agents or model2 not in self.agents:
                raise ValueError("Connections can only be drawn between agents.")
        self.connections: List[Connection] = connections

    def add_connection(self, connection: Connection) -> None:
        (model1, model2) = connection
        if model1 not in self.models or model2 not in self.models:
            raise ValueError("Connections can only be drawn between agents.")
        self.connections.append(connection)

    def remove_connection(self, connection: Connection) -> None:
        if connection not in self.connections:
            raise ValueError("Connection to be removed was not found.")
        self.connections.remove(connection)

    def complete_graph(self) -> None:
        self.connections = [(a, b) for a, b in product(self.models, repeat=2)]

    # def update(self) -> None:
    #     for i, agent in enumerate(self.agents):
    #         candidates = self.hamming_distance_rule(agent)
    #         result = self.tiebreaker_chance(candidates)
    #         self.agents[i] = result

    def hamming_distance_rule(self, agent: Interpretation) -> List[Interpretation]:
        candidates: List[Interpretation] = list()
        candidate_minimum: float = float('inf')

        for model in self.models:
            current_distance: int = 0

            for connection in self.graph[agent]:
                distance_to_agent_model = hamming_distance(model, connection.model)
                current_distance += distance_to_agent_model

            if current_distance < candidate_minimum:
                candidates = [model]
                candidate_minimum = current_distance
            elif current_distance == candidate_minimum:
                candidates.append(model)

        return candidates


    # def tiebreaker_chance(self, interps: List[Interpretation]) -> Interpretation:
    #     return random.choice(interps)


    # def __str__(self):
    #     result = "The graph contains the following agents and their models:\n"

    #     for agent, connections in self.graph.items():
    #         result += f"Agent {agent.name} with models {agent.model}:\n"

    #         for connection in connections:
    #             result += f"  Connected to: {connection.name}, Models: {connection.model}\n"

    #     return result
