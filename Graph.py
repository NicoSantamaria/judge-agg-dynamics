from Agent import *
from BeliefBase import *
from typing import *
import random

type Connection = List[Tuple[int, Agent]]
type GraphEdges = Dict[Agent, List[Connection]]
type UpdateRule = Callable[[Agent], List[Interpretation]]
type TiebreakRule = Callable[[List[Interpretation]], Interpretation]

class Graph:
    def __init__(self, agenda: BeliefBase, agents: list[Agent]=list()) -> None:
        self.agenda: BeliefBase = agenda
        self.graph: GraphEdges = {agent: [] for agent in agents}


    def add_connections(self, agent: Agent, connections: list[Connection]) -> None:
        self.graph[agent] = connections
    

    def remove_connection(self, agent: Agent, connection: Agent) -> None:
        self.graph[agent].remove(connection)


    def complete_graph(self) -> None:
        for agent in self.graph:
            self.add_connections(agent, list(self.graph.keys()))


    def update(self, update_rule: UpdateRule, tiebreaker: TiebreakRule) -> None:
        for agent in self.graph:
            model = tiebreaker(update_rule(agent))
            agent.update_beliefs(model)


    def tiebreaker_chance(self, interps: List[Interpretation]) -> Interpretation:
        return random.choice(interps)
    

    def hamming_distance(self, x: Interpretation, y: Interpretation) -> int:
        count: int = 0

        for a, b in zip(x, y):
            if a != b:
                count += 1

        return count
    

    def hamming_distance_rule(self, agent: Agent) -> List[Interpretation]:
        candidates: List[Interpretation] = list()
        candidate_minimum: int = len(self.agenda.atoms * len(self.graph))

        for model in self.agenda.models:
            current_distance: int = 0

            for connection in self.graph[agent]:
                for agent_model in connection.models:
                    current_distance += self.hamming_distance(model, agent_model)

            if current_distance < candidate_minimum:
                candidates = [model]
                candidate_minimum = current_distance
            elif current_distance == candidate_minimum:
                candidates.append(model)

        res: List[Interpretation] = list()
        agent_minimum: int = candidate_minimum

        for model in candidates:
            for agent_model in agent.models:
                current_distance: int = self.hamming_distance(model, agent_model)

                if current_distance < agent_minimum:
                    res = [model]
                    agent_minimum = current_distance
                elif current_distance == agent_minimum:
                    res.append(model)

        return res
    
    def __str__(self):
        result = "The graph contains the following agents and their models:\n"

        for agent, connections in self.graph.items():
            result += f"Agent {agent.name}:\n"

            for connection in connections:
                result += f"  Connected to: {connection.name}, Models: {connection.models}\n"

        return result
    


IC = BeliefBase(["p", "q", "r"], [["iff", "r", "implies", "p", "q"]])
K1 = Agent(IC, {"p": 1, "q": 1, "r": 1}, "K1")
K2 = Agent(IC, {"p": 1, "q": 0, "r": 0}, "K2")
K3 = Agent(IC, {"p": 0, "q": 0, "r": 1}, "K3")
G = Graph(IC, [K1, K2, K3])
G.complete_graph()
G.remove_connection(K1, K2)

# G.update(G.hamming_distance_rule, G.tiebreaker_chance)