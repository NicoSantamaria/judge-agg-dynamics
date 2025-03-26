from typing import List


def hamming_distance(vec1: List[int], vec2: List[int]) -> int:
    count: int = 0
    for position1, position2 in zip(vec1, vec2):
        if position1 != position2:
            count += 1
    return count
