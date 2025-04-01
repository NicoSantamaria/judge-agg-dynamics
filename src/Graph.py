from random import choice
from typing import List, cast
from itertools import product
from utils.utils import hamming_distance
from utils.types import Interpretation, Connection
from src.BeliefBase import BeliefBase

# TODO: use networkx library to get graphics of each graph
# Potentially we also want to be able to input integers directly, like in beliefbase
# NOTE: after some experimentation, the easier solution is actually probably to only allow integer inputs,
# then convert in the init class
class Graph:
    def __init__(self,
        models: List[Interpretation] | BeliefBase,
        connections: List[Connection]=[],
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
        self.agents: List[Interpretation] = agents

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
        self.connections = [(a, b) for a, b in product(self.agents, repeat=2)]


    def update(self) -> None:
        results: List[Interpretation | None] = [None] * len(self.agents)
        for i, agent in enumerate(self.agents):
            candidates = self.hamming_distance_rule(agent)
            results[i] = choice(candidates)

        if any(res is None for res in results):
            raise ValueError("Update failed.")
        self.agents = cast(List[Interpretation], results)


    def hamming_distance_rule(self, agent: Interpretation) -> List[Interpretation]:
        if agent not in self.agents:
            raise ValueError("Agent not found in graph.")

        candidates: List[Interpretation] = []
        current_min = float('inf')

        for candidate in self.models:
            candidate_distance: int = 0
            for connection in self.connections:
                (agent_model, connection_model) = connection
                if agent_model == agent:
                    candidate_distance += hamming_distance(candidate, connection_model)

            if candidate_distance < current_min:
                candidates = [candidate]
                current_min = candidate_distance
            elif candidate_distance == current_min:
                candidates.append(candidate)

        return candidates

    # DEPRECATED: would like to replace this with networkx draw functions
    def __str__(self):
        result = "The graph contains the following agents and their models:\n"

        for agent, connections in self.graph.items():
            result += f"Agent {agent.name} with models {agent.model}:\n"

            for connection in connections:
                result += f"  Connected to: {connection.name}, Models: {connection.model}\n"

        return result
