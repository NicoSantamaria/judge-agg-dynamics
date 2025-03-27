import pytest
from utils.enums import Z2

def test_Z2():
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
