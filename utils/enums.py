from enum import Enum


class Z2(Enum):
    ZERO = 0
    ONE = 1

    def __new__(cls, value: int):
        obj = object.__new__(cls)
        obj._value_ = value % 2
        return obj

    @classmethod
    def __call__(cls, value):
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

    def __neg__(self) -> 'Z2':
        return self

    def __sub__(self, other: 'Z2') -> 'Z2':
        return self + other

    def __bool__(self) -> bool:
        if self == Z2.ZERO:
            return False
        else:
            return True

    def inverse(self) -> 'Z2':
        if self == Z2.ZERO:
            raise ValueError("Zero has no multiplicative inverse")
        return self

    def __repr__(self) -> str:
        return f"{self}"

class Logic(Enum):
    IMPLIES = "->"
    NOT = "~"
    AND = "&"
    OR = "|"
    IFF = "<->"

    def __call__(self, *args: Z2) -> Z2:
        operations = {
            Logic.NOT: lambda p: not p,
            Logic.IMPLIES: lambda p, q: (not p) or q,
            Logic.AND: lambda p, q: p and q,
            Logic.OR: lambda p, q: p or q,
            Logic.IFF: lambda p, q: p == q
        }

        return operations[self](*args)

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
