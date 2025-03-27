from typing import List
from utils.types import Interpretation, Sentence, Beliefs
from utils.enums import Prop, Logic, Z2


def hamming_distance(vec1: Interpretation, vec2: Interpretation) -> int:
    if len(vec1) != len(vec2):
        raise ValueError("List lengths are not equal.")
    return sum((a.value ^ b.value) for a, b in zip(vec1, vec2))

def ints_to_interpretation(nums: List[int]) -> Interpretation:
    return [Z2(a % 2) for a in nums]

def evaluate_sentence(atoms: List[Prop], interpretation: Interpretation, sentence: Sentence) -> bool:
    if len(atoms) == 0 or len(interpretation) == 0:
        raise ValueError("Empty atoms or interpretation not allowed.")
    if len(atoms) != len(interpretation):
        raise ValueError("The length of the interpretation is not equal to the number of atomic propositions.")
    if sentence == []:
        return True

    stack: List[Z2] = list()
    interp: Beliefs = dict(zip(
        atoms,
        interpretation
    ))

    for char in reversed(sentence):
        if isinstance(char, Logic):
            if char == Logic.NOT:
                first = stack.pop()
                stack.append(char(first))
            else:
                second = stack.pop()
                first = stack.pop()
                stack.append(char(second, first))
        else:
            stack.append(interp[char])

    return bool(stack[0])
