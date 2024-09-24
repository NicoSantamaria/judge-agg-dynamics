"""
What I want this class to do:

1. Init with a given agenda and belief system
2. Connect to other people bidirectionally
3. find which beliefs are found by a supermajority
4. Take the deductive closure on the beliefs
"""
from Boolean import *

class Agent:
    def __init__(self, agenda: 'Boolean'):
        self.connections: list[Agent] = list()
        self.agenda: 'Boolean' = agenda
        self.judgments: set[Sentence] = set()

    def add_connection(self, connection: 'Agent') -> None:
        self.connections.add(connection)
    
    def deductive_closure(self) -> None:
        return
    
    def update_beliefs(self) -> None:
        return