import random
from BeliefBase import *
from typing import *
from AgentFromModels import *

type Models = List[Interpretation]
type GraphFromModels = Dict[AgentFromModels, List[AgentFromModels]]

class GraphFromModels:
    def __init__(self, models: Models, agents: List[AgentFromModels]) -> None:
        self.models: Models = models
        self.graph: GraphFromModels = {agent: [] for agent in agents}


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


    def tiebreaker_chance(self, interps: List[Interpretation]) -> Interpretation:
        return random.choice(interps)


    def hamming_distance(self, x: Interpretation, y: Interpretation) -> int:
        count: int = 0

        for a, b in zip(x, y):
            if a != b:
                count += 1

        return count
    
    # works
    def hamming_distance_rule(self, agent: AgentFromModels) -> List[Interpretation]:
        candidates: List[Interpretation] = list()
        candidate_minimum: float = float('inf')

        for model in self.models:
            current_distance: int = 0

            for connection in self.graph[agent]:
                distance_to_agent_model = self.hamming_distance(model, connection.model)
                current_distance += distance_to_agent_model

            if current_distance < candidate_minimum:
                candidates = [model]
                candidate_minimum = current_distance
            elif current_distance == candidate_minimum:
                candidates.append(model)

        return candidates
    
    
    def __str__(self):
        result = "The graph contains the following agents and their models:\n"

        for agent, connections in self.graph.items():
            result += f"Agent {agent.name} with models {agent.model}:\n"

            for connection in connections:
                result += f"  Connected to: {connection.name}, Models: {connection.model}\n"

        return result
    
    def __eq__(self, other: 'Graph'):
        self_models = set()
        other_models = set()

        for self_agent in self.graph:
            self_models.add(self_agent.models[0])

        for other_agent in other.graph:
            other_models.add(other_agent.models[0])

        return self_models == other_models
    
props = ['p', 'q', 'r']
I = BeliefBase(props, [['iff', 'r', 'implies', 'p', 'q']])

J1 = AgentFromModels((1, 0, 0), 'A')
J2 = AgentFromModels((1, 1, 1), 'B')
J3 = AgentFromModels((0, 0, 1), 'A')

G = GraphFromModels(I.models, [J1, J2, J3])

G.add_connections(J1, [J1, J2, J3])
G.add_connections(J2, [J1, J2])
G.add_connections(J3, [J3])

print(G)

G.hamming_distance_rule(J1)