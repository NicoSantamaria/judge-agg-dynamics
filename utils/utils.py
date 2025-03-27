from typing import List
from utils.types import Interpretation, Sentence, Beliefs
from utils.enums import Prop, Logic, Z2


def hamming_distance(vec1: Interpretation, vec2: Interpretation) -> int:
    if len(vec1) != len(vec2):
        raise ValueError("List lengths are not equal.")
    return sum((a.value ^ b.value) for a, b in zip(vec1, vec2))

def ints_to_interpretation(nums: List[int]) -> Interpretation:
    return [Z2(a % 2) for a in nums]

def strs_to_sentence(strs: List[str]) -> Sentence:
    def symbol_to_enum(symbol: str) -> Prop | Logic:
        try:
            res = Prop(symbol)
            return res
        except ValueError:
            try:
                res = Logic(symbol)
                return res
            except ValueError:
                raise ValueError("Symbol is neither a valid Prop nor Logic.")

    return [symbol_to_enum(symbol) for symbol in strs]

def use_operation(symbol: Logic, *args: Z2) -> Z2:
    operations = {
        Logic.NOT: lambda p: not p,
        Logic.IMPLIES: lambda p, q: (not p) or q,
        Logic.AND: lambda p, q: p and q,
        Logic.OR: lambda p, q: p or q,
        Logic.IFF: lambda p, q: p == q
    }

    return operations[symbol](*args)

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

    for symbol in reversed(sentence):
        if isinstance(symbol, Logic):
            if symbol == Logic.NOT:
                first = stack.pop()
                stack.append(use_operation(symbol, first))
            else:
                second = stack.pop()
                first = stack.pop()
                stack.append(use_operation(symbol, second, first))
        else:
            stack.append(interp[symbol])

    return bool(stack[0])
