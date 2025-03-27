# from src.BeliefBase import BeliefBase

# def test_get_constraints():
#     K = BeliefBase(["p", "q"], [])
#     assert K.constraints == []

#     K = BeliefBase(["p", "q", "r"], [["iff", "r", "implies", "p", "q"]])
#     assert K.constraints == ["iff", "r", "implies", "p", "q"]

#     K = BeliefBase(["p", "q"], [["and", "p", "q"], ["not", "q"]])
#     assert K.constraints == ["and", "and", "p", "q", "not", "q"]

#     K = BeliefBase(["p", "q", "r"], [["not", "p"], ["or", "p", "r"], ["implies", "p", "q"]])
#     assert K.constraints == ["and", "and", "not", "p", "or", "p", "r", "implies", "p", "q"]

# def test_get_models():
#     K = BeliefBase(["p", "q"], [])
#     assert set(K.models) == {(0, 0), (0, 1), (1, 0), (1, 1)}

#     K = BeliefBase(["p", "q"], [["and", "p", "not", "p"]])
#     assert set(K.models) == set()

#     K = BeliefBase(["p", "q", "r"], [["iff", "r", "implies", "p", "q"]])
#     assert set(K.models) == {(1, 1, 1), (0, 0, 1), (1, 0, 0), (0, 1, 1)}

#     K = BeliefBase(["p", "q", "r"], [["not", "p"], ["or", "p", "r"]])
#     assert set(K.models) == {(0, 1, 1), (0, 0, 1)}
