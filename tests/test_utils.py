import pytest
from utils.utils import hamming_distance, evaluate_sentence
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
