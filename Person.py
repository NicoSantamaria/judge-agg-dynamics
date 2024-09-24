"""
What I want this class to do:

1. Init with a given agenda and belief system
2. Connect to other people bidirectionally
3. find which beliefs are found by a supermajority
4. Take the deductive closure on the beliefs
"""
import Agenda

class Person:
    def __init__(self, agenda: 'Agenda'):
        self.agenda: 'Agenda' = agenda
        self.connections: list[Person] = []

    def add_connection(self, connection: 'Person') -> None:
        return
    
    def deductive_closure(self) -> None:
        return
    
    def update_beliefs(self) -> None:
        return