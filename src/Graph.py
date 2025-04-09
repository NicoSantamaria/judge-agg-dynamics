from random import choice
from typing import List, cast
from itertools import product
from utils.utils import hamming_distance
from utils.types import Interpretation, Connection
from src.BeliefBase import BeliefBase

# TODO: use networkx library to get graphics of each graph
# TODO: Allow input by integers
# TODO: implement networkx to draw nice graphs
# TODO: switch order of agents and connections and allow connection to be empty
class Graph:
    """
    Models a social network, where each vertex represents a rational agent holding
    an opinion on the agent, and each edge represents a relationship between rational agents.
    Simulates iterations of the Hamming distance-based aggregation rule.

    ATTRIBUTES:
        models (List[Interpretation]): The set of vectors over Z_2 representing rational
        judgments with respect to the integrity constraints of an agenda.
        connections: List[Connection]: The edges in the graph, representing by ordered
        tuples from one agent to another.
        agents: List[Agent]: The beliefs (as represented by models) by each agent in the
        graph. Agents are represented by vertices in the graph.

    REFERENCES:
    [1] Christian List. The theory of judgment aggregation: An introductory
            review. Synthese, 187(1):179–207, 2012.
    [2] Antonio F. Peralta, János Kertésza, and Gerardo Iñigueza. Opinion dynamics
            in social networks: From models to data. Preprint, 2022. https://arxiv.org/abs/2201.01322
    """
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
        """
        Mutates the graph in-place to add a new edge to the self.connections attribute.

        :param connection: The new edge to be added.
        :return: None
        """
        (first_agent, second_agent) = connection
        num_agents: int = len(self.agents)
        if first_agent >= num_agents or second_agent >= num_agents:
            raise ValueError("Connections can only be drawn between agents.")
        self.connections.append(connection)


    def remove_connection(self, connection: Connection) -> None:
        """
        Mutates the graph in-place to remove the edge from the self.connections attribute.

        :param connection: The edge to be removed.
        :return: None
        """
        if connection not in self.connections:
            raise ValueError("Connection to be removed was not found.")
        self.connections.remove(connection)


    def complete_graph(self) -> None:
        """
        Mutates the graph in-place to add all possible connections between agents.

        :return: None
        """
        num_agents: int = len(self.agents)
        self.connections = [(a, b) for a, b in product(range(num_agents), repeat=2)]


    def update(self) -> None:
        """
        Applies the Hamming distance-based rule to update the beliefs of each
        agent in the graph with respect their connections, breaking ties between
        minimizing models randomly. Mutates the graph in-place.

        :return: None
        """
        self.agents = [choice(self.hamming_distance_rule(i))
            for i in range(len(self.agents))]


    def hamming_distance_rule(self, agent: int) -> List[Interpretation]:
        """
        Computes the Hamming distance-based rule for one specified agent in the graph,
        returning all the minimizing models with respect to that agent and its connections.

        :param agent: The index of the agent for which the Hamming distance-based
        aggregation rule is computed.
        :return: The set of minimizing models for the agent with respect to its connections.
        """
        num_agents: int = len(self.agents)
        if agent < 0 or agent >= num_agents:
            raise ValueError("Agent not found in graph.")

        candidates: List[Interpretation] = []
        current_min = float('inf')

        # Compute the total distance to the relevant agents for each model
        for candidate in self.models:
            candidate_distance: int = 0

            # Find connections to the agent in question and add their models' distance
            for connection in self.connections:
                (first_agent, second_agent) = connection
                second_agent_model = self.agents[second_agent]
                if first_agent == agent:
                    candidate_distance += hamming_distance(candidate, second_agent_model)

            # Only store the minimizing models
            if candidate_distance < current_min:
                candidates = [candidate]
                current_min = candidate_distance
            elif candidate_distance == current_min:
                candidates.append(candidate)

        return candidates
