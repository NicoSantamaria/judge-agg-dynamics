from utils.utils import hamming_distance


def test_hamming_distance():
    assert hamming_distance([], []) == 0
    assert hamming_distance([1], [1]) == 0
    assert hamming_distance([1, 0], [0, 1]) == 2
