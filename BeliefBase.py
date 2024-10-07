from itertools import product

type Sentence = list[chr]
type Interpretation = tuple[int]
type Atoms = dict[chr, int]

class BeliefBase:
    def __init__(self, 
        propositions: list[chr],
        constraints: list[Sentence]=list(),
    ) -> None:
        self.atoms: Atoms = { prop: 1 for prop in propositions }
        self.operations: dict[chr, callable[[bool, bool], bool]] = {
            "¬": lambda p: not p,
            "⇒": lambda p, q: (not p) or q,
            "⇔": lambda p, q: p == q,
            "∧": lambda p, q: p and q,
            "∨": lambda p, q: p or q,
        }

        self.constraints = self.get_constraints(constraints)
        self.models: list[Interpretation] = self.get_models()

    def get_constraints(self, constraints: list[Sentence]) -> Sentence:
        if not constraints:
            return list()
        
        constraint_sentence: Sentence = constraints[0]

        for sentence in constraints[1:]:
            constraint_sentence = self.get_conjunction(
                constraint_sentence,
                sentence
            )

        return constraint_sentence
    
    def get_conjunction(self, sentence1: Sentence, sentence2: Sentence) -> Sentence:
        return ["∧"] + sentence1 + sentence2
    
    def add_constraint(self, sentence: Sentence) -> None:
        self.constraints = self.add_constraint(
            sentence, self.constraints
        )
        

    def evaluate_sentence(self, interpretation: Interpretation, sentence: Sentence) -> bool:
        stack: list[chr] = list()
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
    

    def get_models(self) -> list[Interpretation]:
        models: list[Interpretation] = list()

        for interp in product([0, 1], repeat=len(self.atoms)):

            # constraints shouldn't be a list!
            if self.evaluate_sentence(interp, self.constraints):
                models.append(interp)

        return models
    

# testing
K = BeliefBase(["p", "q", "r", "s"], [["⇔", "r", "⇒", "p", "q"]])
K.models