"""
Belief Base

This class represents belief systems as a set of propositional
sentences under standard logic. Given a number of atomic propositions
and logic constraints on those propositions, the class computes
every combination of truth values that render the given belief system
true with the respect to the constraints. 

Using the parlance of judgment aggregation theory, the class computes
every possible consistent judgment set on a given agenda. 

Logical sentences are understood in Polish notation:

['implies', 'p', 'q'] yields 'p implies q'
"""

from itertools import product
from typing import *

type Sentence = List[str]
type Interpretation = Tuple[int]
type Atoms = Dict[str, int]

class BeliefBase:
    def __init__(self, atoms: Atoms=dict(), constraints: List[Sentence]=list(),) -> None:
        # the atomic propositions
        self.atoms: Atoms = atoms

        # the standard logical operations
        self.operations: Dict[chr, Callable[[bool, bool], bool]] = {
            "¬": lambda p: not p,
            "⇒": lambda p, q: (not p) or q,
            "⇔": lambda p, q: p == q,
            "∧": lambda p, q: p and q,
            "∨": lambda p, q: p or q,
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
        return ["∧"] + sentence1 + sentence2
        

    def evaluate_sentence(self, interpretation: Interpretation, sentence: Sentence) -> bool:
        # evaluate the truth value of a propositional sentence given an interpretation
        # of the atomic propositions, e.g., (1,0) on (p, q) yields false for 
        # 'p implies q'
        stack: List[chr] = list()
        interp: Atoms = dict(zip(
            self.atoms.keys(), 
            interpretation
        ))

        # evaluate the polish notation using the stack
        for char in reversed(sentence):
            if char in self.operations.keys():
                operation = self.operations[char]

                if char == "¬":
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
    

# testing
K = BeliefBase({"p": 1, "q": 1, "r": 1, "s": 1}, [["⇔", "r", "⇒", "p", "q"], ['⇔', 's', '⇒', 'p', 'q']])
K.models