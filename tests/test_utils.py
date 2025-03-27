import pytest
from utils.utils import hamming_distance
from utils.enums import Z2


def test_hamming_distance():
    assert hamming_distance([], []) == 0
    assert hamming_distance([Z2(1)], [Z2(1)]) == 0
    assert hamming_distance([Z2(1), Z2(0)], [Z2(0), Z2(1)]) == 2
    assert hamming_distance([Z2(1), Z2(0), Z2(0),Z2(1)], [Z2(1), Z2(1), Z2(0),Z2(1)]) == 1

    with pytest.raises(ValueError, match="List lengths are not equal."):
        hamming_distance([Z2(1)], [Z2(1), Z2(0)])
    with pytest.raises(ValueError, match="List lengths are not equal."):
        hamming_distance([], [Z2(1), Z2(0), Z2(1)])
