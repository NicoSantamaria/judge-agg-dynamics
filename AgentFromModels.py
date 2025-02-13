from BeliefBase import *
from typing import *


class AgentFromModels:
    def __init__(self, model: Interpretation, name: str="") -> None:
        self.model = model
        self.name = name