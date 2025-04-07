from random import choice
from typing import List, cast
from itertools import product
from utils.utils import hamming_distance
from utils.types import Interpretation, Connection
from src.BeliefBase import BeliefBase

# TODO: use networkx library to get graphics of each graph
# TODO: Allow input by integers
# TODO: implement networkx to draw nice graphs
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

        num_agents: int = len(self.agents)
        for first_agent, second_agent in connections:
            if first_agent >= num_agents or second_agent >= num_agents:
                raise ValueError("Connections can only be drawn between agents.")
        self.connections: List[Connection] = connections


    def add_connection(self, connection: Connection) -> None:
        (first_agent, second_agent) = connection
        num_agents: int = len(self.agents)
        if first_agent >= num_agents or second_agent >= num_agents:
            raise ValueError("Connections can only be drawn between agents.")
        self.connections.append(connection)


    def remove_connection(self, connection: Connection) -> None:
        if connection not in self.connections:
            raise ValueError("Connection to be removed was not found.")
        self.connections.remove(connection)


    def complete_graph(self) -> None:
        num_agents: int = len(self.agents)
        self.connections = [(a, b) for a, b in product(range(num_agents), repeat=2)]


    def update(self) -> None:
        self.agents = [choice(self.hamming_distance_rule(i))
            for i in range(len(self.agents))]


    def hamming_distance_rule(self, agent: int) -> List[Interpretation]:
        num_agents: int = len(self.agents)
        if agent < 0 or agent >= num_agents:
            raise ValueError("Agent not found in graph.")

        candidates: List[Interpretation] = []
        current_min = float('inf')

        for candidate in self.models:
            candidate_distance: int = 0
            for connection in self.connections:
                (first_agent, second_agent) = connection
                second_agent_model = self.agents[second_agent]
                if first_agent == agent:
                    candidate_distance += hamming_distance(candidate, second_agent_model)

            if candidate_distance < current_min:
                candidates = [candidate]
                current_min = candidate_distance
            elif candidate_distance == current_min:
                candidates.append(candidate)

        return candidates

    # DEPRECATED: would like to replace this with networkx draw functions
    # def __str__(self):
    #     result = "The graph contains the following agents and their models:\n"

    #     for agent, connections in self.graph.items():
    #         result += f"Agent {agent.name} with models {agent.model}:\n"

    #         for connection in connections:
    #             result += f"  Connected to: {connection.name}, Models: {connection.model}\n"

    #     return result
