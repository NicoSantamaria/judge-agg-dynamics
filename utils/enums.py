from enum import Enum


class Z2(Enum):
    ZERO = 0
    ONE = 1

    def __new__(cls, value: int):
        value %= 2
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, int):
            return cls(value % 2)
        raise ValueError("Z2 values must be of type int.")

    @classmethod
    def __call__(cls, value: int):
        value %= 2
        if value == 0:
            return cls.ZERO
        elif value == 1:
            return cls.ONE
        else:
            raise ValueError(f"{value} not valid in Z2.")

    def __add__(self, other: 'Z2') -> 'Z2':
        return Z2(self.value ^ other.value)

    def __mul__(self, other: 'Z2') -> 'Z2':
        return Z2(self.value & other.value)

    def __bool__(self) -> bool:
        if self == Z2.ZERO:
            return False
        else:
            return True

    def __repr__(self) -> str:
        return f"{self}"

class Logic(Enum):
    IMPLIES = "->"
    NOT = "~"
    AND = "&"
    OR = "|"
    IFF = "<->"


class Prop(Enum):
    P = "p"
    Q = "q"
    R = "r"
    S = "s"
    T = "t"
    U = "u"
    V = "v"
    W = "w"
    X = "x"
    Y = "y"
    Z = "z"
