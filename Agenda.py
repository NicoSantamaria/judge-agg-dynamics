"""
What I want this class to do

Represent the agenda as a field of boolean sentences,
using the Boolean class, with negations
"""
import Boolean

class Agenda:
    def __init__(self, propositions: list[chr], sentences: list[chr]):
        self.agenda = Boolean(propositions)

        for sentence in sentences:
            self.agenda.add_sentence(sentence)
            self.agenda.add_sentence(["not"] + sentence)
