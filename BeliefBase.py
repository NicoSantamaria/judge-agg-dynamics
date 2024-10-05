from itertools import product

type Sentence = list[chr]
type Interpretation = tuple[int]
type Atoms = dict[chr, int]

class BeliefBase:
    def __init__(self, propositions: list[chr]) -> None:
        self.atoms: Atoms = {prop: 1 for prop in propositions}
        self.constraints: list[Sentence] = []
        self.models: list[Interpretation] = []

        self.interpretations: list[Interpretation] = list(
            product([0, 1], repeat=len(self.atoms))
        )

        self.operations: dict[chr, callable[[bool, bool], bool]] = {
            "¬": lambda p: not p,
            "⇒": lambda p, q: (not p) or q,
            "⇔": lambda p, q: p == q,
            "∧": lambda p, q: p and q,
            "∨": lambda p, q: p or q,
        }


    def add_constraint(self, sentence: Sentence) -> None:
        """
        This should actually add each new constraint in conjunction with the previous constraints
        """
        self.constraints.append(sentence)


    def evaluate_sentence(self, interpretation: Interpretation, sentence: Sentence) -> bool:
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

                stack.append(operation(second, first))
            else:
                stack.append(interp[char])

        return stack[0]
    
    def get_models(self) -> None:
        for interp in self.interpretations:

            # constraints shouldn't be a list!
            if self.evaluate_sentence(interp, self.constraints[0]):
                self.models.append(interp)
    

# testing
K = BeliefBase(["p", "q", "r"])
K.add_constraint(["⇔", "r", "⇒", "p", "q"])
K.get_models()
K.models