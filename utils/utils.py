from src.AgentFromModels import Interpretation


def hamming_distance(vec1: Interpretation, vec2: Interpretation) -> int:
    count: int = 0
    for position1, position2 in zip(vec1, vec2):
        if position1 != position2:
            count += 1
    return count
