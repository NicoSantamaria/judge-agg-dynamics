from BeliefBase import *
from typing import *

type Sentence = List[str]
type Interpretation = Tuple[int]
type Atoms = List[str]
type Beliefs = Dict[str, int]

class Agent:
    def __init__(self, agenda: BeliefBase, beliefs: Beliefs=dict()) -> None:
        # the agenda gives the atomic propositions and the logical constraints on the agent
        self.agenda: BeliefBase = agenda

        # The agent's 'take' on the atomic propositions. -1 represents a suspension of judgment
        # on the proposition
        self.beliefs: Beliefs = beliefs

        # The models for the agent's belief system
        self.models: List[Interpretation] = self.get_models()

    def get_models(self) -> List[Interpretation]:
        models: List[Interpretation] = list()

        # pull from the models which satisfy the integrity constraints
        for interp in self.agenda.models:

            # tracks if the current interpretation is a valid model
            candidate: bool = True

            # check that the current interp represents the agent's beliefs
            for i, value in enumerate(interp):
                prop: str = self.agenda.atoms[i]
                match: int = self.beliefs[prop]

                # if the agent has made a judgment on the prop and the interp
                # does not match that judgment, then the interp is not a candidate
                if match != -1 and match != value:
                    candidate = False
                    break

            # add to agent models if the interp matches the agent's beliefs
            if candidate:
                models.append(interp)

        return models
    
    def update_beliefs(self, beliefs: Beliefs) -> None:
        self.beliefs = beliefs
        self.models = self.get_models()
        
# testing
IC = BeliefBase(["p", "q", "r", "s"], [["iff", "r", "and", "p", "q"], ['iff', 's', 'not', 'or', 'p', 'r']])
K = Agent(IC, {"p": 0, "q": 0, "r": -1, "s": 0})
K.models