import pytest
from utils.enums import Z2, Logic, Prop

def test_Z2():
    assert Z2(0) == Z2.ZERO
    assert Z2(1) == Z2.ONE
    assert Z2(3) == Z2.ONE
    assert Z2(3) == Z2(1)
    assert Z2(2) == Z2(0)
    assert Z2(3) != Z2(4)
    assert Z2(-1) == Z2(1)
    assert Z2(0) != Z2(1)
    assert Z2(1) + Z2(0) == Z2(1)
    assert Z2(4) + Z2(2) == Z2(0)
    assert Z2(-3) + Z2(1) == Z2(0)
    assert Z2(1) * Z2(0) == Z2(0)
    assert Z2(1) * Z2(1) == Z2(1)
    assert Z2(-1) * Z2(5) == Z2(1)
    assert Z2(2) * Z2(2) == Z2(0)
    assert bool(Z2(1)) == True
    assert bool(Z2(0)) == False
    assert bool(Z2(-5)) == True

    with pytest.raises(ValueError, match="Z2 values must be of type int."):
        Z2(4.0)
    with pytest.raises(ValueError, match="Z2 values must be of type int."):
        Z2("ag")

def test_logic():
    assert Logic("->") == Logic.IMPLIES
    assert Logic("<->") == Logic.IFF
    assert Logic("&") == Logic.AND
    assert Logic("|") == Logic.OR
    assert Logic("~") == Logic.NOT

    value = "a"
    with pytest.raises(ValueError, match=f"{value} not a valid value in Logic."):
        Logic(value)

    value = "g3"
    with pytest.raises(ValueError, match=f"{value} not a valid value in Logic."):
        Logic(value)

    with pytest.raises(ValueError, match="Logic values must be of type str."):
        Logic(-1)

    with pytest.raises(ValueError, match="Logic values must be of type str."):
        Logic(True)

def test_prop():
    assert Prop("p") == Prop.P
    assert Prop("r") == Prop.R
    assert Prop("s") == Prop.S

    value = "a"
    with pytest.raises(ValueError, match=f"{value} not a valid value in Prop."):
        Prop(value)

    value = "2g3d"
    with pytest.raises(ValueError, match=f"{value} not a valid value in Prop."):
        Prop(value)

    with pytest.raises(ValueError, match="Prop values must be of type str."):
        Prop(5.2)

    with pytest.raises(ValueError, match="Prop values must be of type str."):
        Prop(0)
