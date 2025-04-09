from itertools import product
from typing import List
from utils.utils import evaluate_sentence
from utils.enums import Z2, Prop, Logic
from utils.types import Sentence, Interpretation


# TODO: allow input by strs instead of props
class BeliefBase:
    """
    A `belief base` contains a set of atomic propositions, a set of rational
    constraints on those propositions called `integrity constraints,` and a set
    of vectors over Z_2 representing rational assignments of truth values to the
    atomic propositions with respect to the integrity constraints.

    ATTRIBUTES:
        atoms (List[Prop]): The atomic propositions in the agenda.
        constraints (Sentence): The conjunction of propositional sentence in the
        set of integrity constraints.
        models (List[Interpretation]): The vectors representing rational assignments
        of truth values to the atomic propositions with respect to the integrity constraints

    REFERENCES:
    [1] Gabriella Pigozzi. Belief merging and the discursive dilemma: an
            argument-based account to paradoxes of judgment aggregation. Synthese,
            152(2):285–98, 2006.
    """
    def __init__(self, atoms: List[Prop], constraints: List[Sentence]=list()) -> None:
        self.atoms: List[Prop] = atoms
        self.constraints: Sentence = self.get_constraints(constraints)
        self.models: List[Interpretation] = self.get_models()


    @staticmethod
    def get_constraints(constraints: List[Sentence]) -> Sentence:
        """
        Any rational interpretation of the atomic propositions with respect to the
        propositional sentences in the set of integrity constraints also satisfies the
        single conjunction of sentences in the set of integrity constraints. Returns the
        single conjunctive sentences from the set of propositional sentences forming the
        integrity constraints.

        :param constraints: The propositional sentences in the set of integrity constraints.
        :return: The conjunction of sentences in the set of integrity constraints.
        """
        if not constraints:
            return list()

        # Build the single conjunctive sentence from the sentences in the integrity constraints.
        constraint_sentence: Sentence = constraints[0]
        for sentence in constraints[1:]:
            constraint_sentence = [Logic.AND] + constraint_sentence + sentence
        return constraint_sentence


    def get_models(self) -> List[Interpretation]:
        """
        Models are assignments of truth values to the atomic propositions in the belief base
        which render the conjunctive sentence of integrity constraints true.

        :return: A list of vectors over Z_2 representing rational assignments of truth values
        to the atomic propositions with respect to the integrity constraints.
        """
        models: List[Interpretation] = list()

        # Brute force check every possible assignment of truth values
        for interp in product([Z2(0), Z2(1)], repeat=len(self.atoms)):
            interp_list = list(interp)
            if not self.constraints or evaluate_sentence(self.atoms, interp_list, self.constraints):
                models.append(interp_list)
        return models
