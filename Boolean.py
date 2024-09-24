"""
What do I want this class to do?

For now:
1. init with a number of field variables (i.e., p, q, r, etc.)
2. store an array of arbitrary boolean sentences
3. create a truth table for an arbitrary boolean sentence
4. check logical equivalence between arbitrary boolean sentences

"""
type Sentence = list[str]
type TruthTable = list[bool]

class Boolean:
    def __init__(self, propositions: list[str]) -> None:
        self.sentences = dict[Sentence, TruthTable] = {p: [0, 1] for p in propositions}
        self.operations: dict[str, callable[[bool, bool], bool]] = {
            "not": lambda p: not p,
            "and": lambda p, q: p and q,
            "or": lambda p, q: p or q,
            "implies": lambda p, q: (not p) or q,
        }

    def add_sentence(sentence: list[str]) -> None:
        return
    
    def add_proposition(self, proposition: list[str]) -> None:
        self.sentences[proposition] = [0, 1]

    def __str__(self) -> None:
        # Print all propositions with truth tables
        return