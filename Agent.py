from BeliefBase import *
from typing import *

type Sentence = List[str]
type Interpretation = Tuple[int]
type Atoms = List[str]
type Beliefs = Dict[str, int]

class Agent:
    def __init__(self, agenda: BeliefBase, beliefs: Beliefs=dict()) -> None:
        self.agenda: BeliefBase = agenda
        self.beliefs: Beliefs = beliefs 

    def get_models(self) -> List[Interpretation]:
        models: List[Interpretation] = list()

        for interp in product([0, 1], repeat=len(self.agenda.atoms)):
            candidate: bool = True

            for i, value in enumerate(interp):
                prop: str = self.agenda.atoms[i]
                match: int = self.beliefs[prop]

                if match != -1 and match != value:
                    candidate = False
                    break

            if candidate:
                eval = self.agenda.evaluate_sentence(
                    interp, self.agenda.constraints
                )

                if eval:
                    models.append(interp)

        return models
        
# testing
IC = BeliefBase(["p", "q", "r", "s"], [["⇔", "r", "⇒", "p", "q"], ['⇔', 's', '∧', 'p', 'q']])
K = Agent(IC, {"p": 0, "q": 0, "r": 1, "s": -1})
K.get_models()

# Expect: [(0, 0, 1, 0)]