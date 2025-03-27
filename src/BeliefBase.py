from itertools import product
from typing import List, Dict, Callable

type Sentence = List[str]
type Interpretation = List[int]
type Atoms = List[str]
type Beliefs = Dict[str, int]

class BeliefBase:
    def __init__(self, atoms: Atoms, constraints: List[Sentence]=list(),) -> None:
        # the atomic propositions with interpretations.
        # -1 represents a "no judgment"
        self.atoms: List[str] = atoms

        # the standard logical operations
        self.operations: Dict[str, Callable] = {
            "not": lambda p: not p,
            "implies": lambda p, q: (not p) or q,
            "iff": lambda p, q: p == q,
            "and": lambda p, q: p and q,
            "or": lambda p, q: p or q,
        }

        # computes the set of logical constraints as a single conjunctive
        # propositional sentence; this makes it easier to find models
        self.constraints = self.get_constraints(constraints)

        # computes all the combinations of truth-values on the atomic propositions
        # that satisfy the constraints: stores the models as binary tuples
        self.models: list[Interpretation] = self.get_models()

    def get_constraints(self, constraints: list[Sentence]) -> Sentence:
        # build the single conjunctive sentence from the list of
        # given constraints.
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
        # represent the conjunction of two sentences in Polish Notation
        return ["and"] + sentence1 + sentence2


    def evaluate_sentence(self, interpretation: Interpretation, sentence: Sentence) -> bool:
        # evaluate the truth value of a propositional sentence given an interpretation
        # of the atomic propositions, e.g., (1,0) on (p, q) yields false for
        # 'p implies q'
        stack: List[str] = list()
        interp: Beliefs = dict(zip(
            self.atoms,
            interpretation
        ))

        # evaluate the polish notation using the stack
        for char in reversed(sentence):
            if char in self.operations.keys():
                operation = self.operations[char]

                if char == "not":
                    first = stack.pop()
                    stack.append(operation(first))
                else:
                    second = stack.pop()
                    first = stack.pop()
                    stack.append(operation(second, first))
            else:
                stack.append(interp[char])

        return stack[0]


    def get_models(self) -> List[Interpretation]:
        # compute all the combinations of truth-values for the atomic
        # propositions which satisfy the constraints
        models: List[Interpretation] = list()

        for interp in product([0, 1], repeat=len(self.atoms)):
            if not self.constraints or self.evaluate_sentence(interp, self.constraints):
                models.append(interp)

        return models
