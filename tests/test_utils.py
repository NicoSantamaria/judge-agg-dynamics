from utils.utils import hamming_distance


def test_hamming_distance():
    assert hamming_distance([], []) == 0
