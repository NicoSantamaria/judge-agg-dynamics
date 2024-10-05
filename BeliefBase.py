type Sentence = list[chr]
type Interpretations = tuple[int]
type Atoms = dict[chr, int]

class BeliefBase:
    def __init__(self, propositions: list[chr]) -> None:
        self.atoms: Atoms = {prop: 1 for prop in propositions}
        self.constraints: list[Sentence] = []
        self.interpretations: list[Interpretations] = []
        self.models: list[Interpretations] = []
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
        stack: list[chr] = []
        interp: Atoms = dict(zip(
            self.atoms.keys(), 
            interpretation
        ))

        for char in sentence[::-1]:
            if char in self.operations.keys():
                operation = self.operations[char]
                second = stack.pop()
                first = stack.pop()

                stack.append(operation(first, second))
            else:
                stack.append(interp[char])

        return stack[0]
    
    def get_models(self) -> None:
        return
    

# testing
K = BeliefBase(["p", "q", "r"])
K.add_constraint(["⇔", "r", "⇒", "p", "q"])