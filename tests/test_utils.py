import pytest
from utils.utils import hamming_distance, evaluate_sentence, ints_to_interpretation, strs_to_sentence
from utils.enums import Z2, Logic, Prop


def test_hamming_distance():
    assert hamming_distance([], []) == 0
    assert hamming_distance([Z2(1)], [Z2(1)]) == 0
    assert hamming_distance([Z2(1), Z2(0)], [Z2(0), Z2(1)]) == 2
    assert hamming_distance([Z2(1), Z2(0), Z2(0),Z2(1)], [Z2(1), Z2(1), Z2(0),Z2(1)]) == 1

    with pytest.raises(ValueError, match="List lengths are not equal."):
        hamming_distance([Z2(1)], [Z2(1), Z2(0)])
    with pytest.raises(ValueError, match="List lengths are not equal."):
        hamming_distance([], [Z2(1), Z2(0), Z2(1)])

def test_evaluate_sentence():
    assert evaluate_sentence([Prop.P], [Z2(0)], []) == True
    assert evaluate_sentence([Prop.P, Prop.Q], [Z2(1), Z2(0)], []) == True
    assert evaluate_sentence([Prop.P, Prop.Q], [Z2(1), Z2(0)], [Logic.IFF, Prop.P, Prop.Q]) == False
    assert evaluate_sentence([Prop.P, Prop.Q], [Z2(1), Z2(1)], [Logic.IFF, Prop.P, Prop.Q]) == True
    assert evaluate_sentence([Prop.P, Prop.Q], [Z2(0), Z2(0)], [Logic.IFF, Prop.P, Prop.Q]) == True
    assert evaluate_sentence([Prop.P, Prop.Q, Prop.R], [Z2(1), Z2(0), Z2(1)], [Logic.AND, Prop.P, Prop.Q]) == False
    assert evaluate_sentence([Prop.P, Prop.Q, Prop.R], [Z2(1), Z2(1), Z2(1)], [Logic.AND, Prop.P, Prop.Q]) == True
    assert evaluate_sentence([Prop.P, Prop.Q, Prop.R], [Z2(1), Z2(1), Z2(1)], [Logic.AND, Logic.NOT, Prop.P, Prop.Q]) == False
    assert evaluate_sentence([Prop.P, Prop.Q, Prop.R], [Z2(1), Z2(0), Z2(1)], [Logic.OR, Prop.P, Prop.Q]) == True
    assert evaluate_sentence([Prop.P, Prop.Q, Prop.R], [Z2(1), Z2(0), Z2(1)], [Logic.IMPLIES, Prop.P, Prop.Q]) == False
    assert evaluate_sentence([Prop.P, Prop.Q, Prop.R, Prop.S], [Z2(1), Z2(0), Z2(1), Z2(0)], [Logic.AND, Logic.OR, Prop.P, Prop.Q, Logic.OR, Prop.R, Prop.S]) == True

    with pytest.raises(ValueError, match="Empty atoms or interpretation not allowed."):
        assert evaluate_sentence([], [], [])
    with pytest.raises(ValueError, match="The length of the interpretation is not equal to the number of atomic propositions."):
        assert evaluate_sentence([Prop.P, Prop.Q], [Z2(1), Z2(0), Z2(1)], [])

def test_ints_to_interpretation():
    assert ints_to_interpretation([]) == []
    assert ints_to_interpretation([1, 0, 1]) == [Z2(1), Z2(0), Z2(1)]
    assert ints_to_interpretation([0, 0]) == [Z2(0), Z2(0)]
    assert ints_to_interpretation([3, 2, 1]) == [Z2(1), Z2(0), Z2(1)]

def test_strs_to_sentence():
    assert strs_to_sentence([]) == []
    assert strs_to_sentence(["&", "p", "q"]) == [Logic.AND, Prop.P, Prop.Q]
    assert strs_to_sentence(["<->", "r", "->", "p", "q"]) == [Logic.IFF, Prop.R, Logic.IMPLIES, Prop.P, Prop.Q]

    with pytest.raises(ValueError, match="Symbol is neither a valid Prop nor Logic."):
        strs_to_sentence(["&", "2g4g", "q"])

    with pytest.raises(ValueError, match="Symbol is neither a valid Prop nor Logic."):
        strs_to_sentence(["sd"])
