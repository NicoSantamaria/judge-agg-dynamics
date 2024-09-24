"""
What do I want this class to do?

For now:
1. init with a number of field variables (i.e., p, q, r, etc.)
2. store an array of arbitrary boolean sentences
3. create a truth table for an arbitrary boolean sentence
4. check logical equivalence between arbitrary boolean sentences

"""

class Boolean:
    def __init__(self, propositions: list[chr]) -> None:
        self.propositions = propositions
        self.sentences: list[chr] = []
        self.operations: dict[str, callable[[bool, bool], bool]] = {
            "not": lambda p: not p,
            "and": lambda p, q: p and q,
            "or": lambda p, q: p or q,
            "implies": lambda p, q: (not p) or q,
        }

    def add_sentence(sentence: list[chr]) -> None:
        return