import numpy as np
from typing import List
# remove beliefs
from utils.types import Interpretation, Sentence, Beliefs, Matrix, MatrixZ2
from utils.enums import Prop, Logic, Z2


def hamming_distance(vec1: Interpretation, vec2: Interpretation) -> int:
    if len(vec1) != len(vec2):
        raise ValueError("List lengths are not equal.")
    return sum((a.value ^ b.value) for a, b in zip(vec1, vec2))

def ints_to_interpretation(nums: List[int]) -> Interpretation:
    return [Z2(a % 2) for a in nums]

def interpretation_to_ints(interp: Interpretation) -> List[int]:
    return [0 if z == Z2.ZERO else 1 for z in interp]

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
    if len(args) == 0:
        raise ValueError("The function use_operation must be passed at least one argument of type Z2.")
    operations = {
        Logic.NOT: lambda p: not p,
        Logic.IMPLIES: lambda p, q: (not p) or q,
        Logic.AND: lambda p, q: p and q,
        Logic.OR: lambda p, q: p or q,
        Logic.IFF: lambda p, q: p == q
    }

    if symbol == Logic.NOT:
        if len(args) != 1:
            raise ValueError("NOT operation takes exactly 1 argument.")
        res = operations[symbol](args[0])
    else:
        if len(args) != 2:
            raise ValueError("AND, OR, IFF, and IMPLIES operations take exactly 2 arguments.")
        res = operations[symbol](args[0], args[1])

    if isinstance(res, bool):
        return Z2.ONE if res else Z2.ZERO
    return res

def evaluate_sentence(atoms: List[Prop], interpretation: Interpretation, sentence: Sentence) -> bool:
    if len(atoms) == 0 or len(interpretation) == 0:
        raise ValueError("Empty atoms or interpretation not allowed.")
    if len(atoms) != len(interpretation):
        raise ValueError("The length of the interpretation is not equal to the number of atomic propositions.")
    if sentence == []:
        return True

    # rewrite without beliefs (more efficient too)
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

def matrix_z2_to_matrix(mat: MatrixZ2) -> Matrix:
    if np.array_equal(mat, np.array([])):
        return np.array([])

    rows, cols = mat.shape
    res = np.ones((rows, cols))
    for i in range(rows):
        for j in range(cols):
            if mat[i, j] == Z2.ZERO:
                res[i, j] = 0
    return res

def matrix_to_matrix_z2(mat: Matrix) -> MatrixZ2:
    if np.array_equal(mat, np.array([])):
        return np.array([])

    rows, cols = mat.shape
    res: MatrixZ2 = np.empty((rows, cols), dtype=object)
    for i in range(rows):
        for j in range(cols):
            if mat[i, j] == 0:
                res[i, j] = Z2.ZERO
            else:
                res[i, j] = Z2.ONE
    return res