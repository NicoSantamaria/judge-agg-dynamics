from itertools import product
from typing import List
from utils.utils import evaluate_sentence
from utils.enums import Z2, Prop, Logic
from utils.types import Sentence, Interpretation


class BeliefBase:
    def __init__(self, atoms: List[Prop], constraints: List[Sentence]=list(),) -> None:
        self.atoms: List[Prop] = atoms
        self.constraints: Sentence = self.get_constraints(constraints)
        self.models: List[Interpretation] = self.get_models()

    def get_constraints(self, constraints: List[Sentence]) -> Sentence:
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
        return [Logic.AND] + sentence1 + sentence2


    def get_models(self) -> List[Interpretation]:
        models: List[Interpretation] = list()
        for interp in product([Z2(0), Z2(1)], repeat=len(self.atoms)):
            interp_list = list(interp)
            if not self.constraints or evaluate_sentence(self.atoms, interp_list, self.constraints):
                models.append(interp_list)
        return models
