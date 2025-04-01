import numpy as np
from typing import List, Tuple, Dict, TypeAlias
from numpy.typing import NDArray
from utils.enums import Z2, Logic, Prop

type Interpretation = List[Z2]
type Sentence = List[Logic | Prop]
type Beliefs = Dict[Prop, Z2]
type Connection = Tuple[Interpretation, Interpretation]
type Matrix = NDArray
MatrixZ2: TypeAlias = NDArray[np.object_]
