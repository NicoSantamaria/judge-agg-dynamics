from utils.types import Interpretation


def hamming_distance(vec1: Interpretation, vec2: Interpretation) -> int:
    if len(vec1) != len(vec2):
        raise ValueError("List lengths are not equal.")
    return sum((a.value ^ b.value) for a, b in zip(vec1, vec2))


# def model_from_interpretation(interp: Interpretation) -> List[int]:
#     return []
