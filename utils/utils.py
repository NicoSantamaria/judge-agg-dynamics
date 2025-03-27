from .types import Interpretation


def hamming_distance(vec1: Interpretation, vec2: Interpretation) -> int:
    return sum((a.value ^ b.value) for a, b in zip(vec1, vec2))


# def model_from_interpretation(interp: Interpretation) -> List[int]:
#     return []
