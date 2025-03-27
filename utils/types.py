from typing import List, Dict
from numpy import ndarray
from enums import Z2, Logic, Proposition

type Interpretation = List[Z2]
type Sentence = List[Logic | Proposition]
type Beliefs = Dict[Proposition, Z2]
type Matrix = ndarray
