import random
from BeliefBase import Interpretation
from typing import List, Dict
from AgentFromModels import AgentFromModels
from utils.utils import hamming_distance

type Models = List[Interpretation]
type GraphFromModelsType = Dict[AgentFromModels, List[AgentFromModels]]

class GraphFromModels:
    def __init__(self, models: Models, agents: List[AgentFromModels]) -> None:
        self.models: Models = models
        self.graph: GraphFromModelsType = {agent: [] for agent in agents}


    def add_connections(self, agent: AgentFromModels, connections: List[AgentFromModels]) -> None:
        self.graph[agent] = connections


    def remove_connection(self, agent: AgentFromModels, connections: List[AgentFromModels]) -> None:
        for connection in connections:
            self.graph[agent].remove(connection)


    def complete_graph(self) -> None:
        for agent in self.graph:
            self.add_connections(agent, list(self.graph.keys()))


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
