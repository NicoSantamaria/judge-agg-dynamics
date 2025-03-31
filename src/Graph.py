import random
from typing import List
from itertools import product
from utils.types import Interpretation, Connection
from src.BeliefBase import BeliefBase


class Graph:
    def __init__(self, models: List[Interpretation] | BeliefBase, connections: List[Connection]) -> None:
        self.models: List[Interpretation] = []
        if isinstance(models, BeliefBase):
            self.models = models.models
        else:
            self.models = models

        for model1, model2 in connections:
            if model1 not in self.models or model2 not in self.models:
                raise ValueError("Connections can only be drawn between models.")
        self.connections: List[Connection] = connections

    def add_connections(self, connection: Connection) -> None:
        (model1, model2) = connection
        if model1 not in self.models or model2 not in self.models:
            raise ValueError("Connections can only be drawn between models.")
        self.connections.append(connection)

    def remove_connection(self, connection: Connection) -> None:
        if connection not in self.connections:
            raise ValueError("Connection to be removed was not found.")
        self.connections.remove(connection)

    def complete_graph(self) -> None:
        self.connections = [(a, b) for a, b in product(self.models, repeat=2)]


    def update(self) -> None:
        results = []

        for agent in self.graph:
            candidates = self.hamming_distance_rule(agent)
            result = self.tiebreaker_chance(candidates)
            results.append(result)

        for i, agent in enumerate(self.graph):
            agent.update_beliefs(results[i])


    def hamming_distance_rule(self, agent: AgentFromModels) -> List[Interpretation]:
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


    def tiebreaker_chance(self, interps: List[Interpretation]) -> Interpretation:
        return random.choice(interps)


    def __str__(self):
        result = "The graph contains the following agents and their models:\n"

        for agent, connections in self.graph.items():
            result += f"Agent {agent.name} with models {agent.model}:\n"

            for connection in connections:
                result += f"  Connected to: {connection.name}, Models: {connection.model}\n"

        return result
