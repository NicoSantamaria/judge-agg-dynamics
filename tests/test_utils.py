from utils.utils import hamming_distance
from utils.enums import Z2


def test_hamming_distance():
    assert hamming_distance([], []) == 0
    assert hamming_distance([Z2(1)], [Z2(1)]) == 0
    assert hamming_distance([Z2(1), Z2(0)], [Z2(0), Z2(1)]) == 2
