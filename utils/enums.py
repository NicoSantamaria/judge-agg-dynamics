from enum import Enum

class Z2(Enum):
    ZERO = 0
    ONE = 1

    def __add__(self, other: 'Z2') -> 'Z2':
        return Z2(self.value ^ other.value)

    def __mul__(self, other: 'Z2') -> 'Z2':
        return Z2(self.value & other.value)

    def __neg__(self) -> 'Z2':
        return self

    def __sub__(self, other: 'Z2') -> 'Z2':
        return self + other

    def inverse(self) -> 'Z2':
        if self == Z2.ZERO:
            raise ValueError("Zero has no multiplicative inverse")
        return self

    def __repr__(self) -> str:
        return f"{self}"

class Logic(Enum):
    IMPLIES = ">"
    NOT = "~"
    AND = "&"
    OR = "|"

class Proposition(Enum):
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
