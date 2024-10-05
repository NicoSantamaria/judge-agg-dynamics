type Sentence = list[chr]
type model = tuple[int]

class BeliefBase:
    def __init__(self, propositions: list[chr]) -> None:
        self.atoms: list[chr] = propositions
        self.constraints: list[Sentence] = []
        self.models: list[model] = []
        self.operations: dict[chr, callable[[bool, bool], bool]] = {
            "¬": lambda p: not p,
            "⇒": lambda p, q: (not p) or q,
            "⇔": lambda p, q: p == q,
            "∧": lambda p, q: p and q,
            "∨": lambda p, q: p or q,
        }

    def add_constraint(self, sentence: Sentence) -> None:
        self.constraints.append(sentence)
        self.get_models()

    def evaluate_sentence(self, interpretation: list[int], sentence: Sentence) -> bool:
        return True
    
    def get_models(self) -> None:
        return