from src.jaggdy.BeliefBase import BeliefBase
from src.jaggdy.utils.enums import Logic, Prop, Z2

def test_get_constraints():
    K = BeliefBase([Prop.P, Prop.Q], [])
    assert K.constraints == []

    K = BeliefBase([Prop.P, Prop.Q, Prop.R], [[Logic.IFF, Prop.R, Logic.IMPLIES, Prop.P, Prop.Q]])
    assert K.constraints == [Logic.IFF, Prop.R, Logic.IMPLIES, Prop.P, Prop.Q]

    K = BeliefBase([Prop.P, Prop.Q], [[Logic.AND, Prop.P, Prop.Q], [Logic.NOT, Prop.Q]])
    assert K.constraints == [Logic.AND, Logic.AND, Prop.P, Prop.Q, Logic.NOT, Prop.Q]

    K = BeliefBase([Prop.P, Prop.Q, Prop.R], [[Logic.NOT, Prop.P], [Logic.OR, Prop.P, Prop.R], [Logic.IMPLIES, Prop.P, Prop.Q]])
    assert K.constraints == [Logic.AND, Logic.AND, Logic.NOT, Prop.P, Logic.OR, Prop.P, Prop.R, Logic.IMPLIES, Prop.P, Prop.Q]

def test_get_models():
    def make_set(models):
        return set(tuple(model) for model in K.models)

    K = BeliefBase([Prop.P, Prop.Q], [])
    assert make_set(K.models) == make_set([[Z2(0), Z2(0)], [Z2(0), Z2(1)], [Z2(1), Z2(0)], [Z2(1), Z2(1)]])

    K = BeliefBase([Prop.P, Prop.Q], [[Logic.AND, Prop.P, Logic.NOT, Prop.P]])
    assert make_set(K.models) == set()

    K = BeliefBase([Prop.P, Prop.Q, Prop.R], [[Logic.IFF, Prop.R, Logic.IMPLIES, Prop.P, Prop.Q]])
    assert make_set(K.models) == make_set([[Z2(1), Z2(1), Z2(1)], [Z2(0), Z2(0), Z2(1)], [Z2(1), Z2(0), Z2(0)], [Z2(0), Z2(1), Z2(1)]])

    K = BeliefBase([Prop.P, Prop.Q, Prop.R], [[Logic.NOT, Prop.P], [Logic.OR, Prop.P, Prop.R]])
    assert make_set(K.models) == make_set([[Z2(0), Z2(1), Z2(1)], [Z2(0), Z2(0), Z2(1)]])
