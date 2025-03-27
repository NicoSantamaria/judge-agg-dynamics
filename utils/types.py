from typing import List, Dict
from numpy import ndarray
from utils.enums import Z2, Logic, Prop

type Interpretation = List[Z2]
type Sentence = List[Logic | Prop]
type Beliefs = Dict[Prop, Z2]
type Matrix = ndarray
