from typing import List, Dict, Tuple
from numpy import ndarray
from utils.enums import Z2, Logic, Prop

type Interpretation = List[Z2]
type Sentence = List[Logic | Prop]
type Matrix = ndarray
type Connection = Tuple[Interpretation, Interpretation]
