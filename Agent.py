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
        # if the judgment set is complete, there is one model given directly
        # by the beliefs
        if -1 not in self.beliefs.values():
            return self.beliefs.values()
        
        models: List[Interpretation] = list()

        # brute force the possible intepretations on the propositions
        for interp in product([0, 1], repeat=len(self.agenda.atoms)):

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

            if candidate:
                # check that the candidate satisfies the agenda's constraints
                eval = self.agenda.evaluate_sentence(
                    interp, self.agenda.constraints
                )

                if eval:
                    models.append(interp)

        return models
        
# testing
IC = BeliefBase(["p", "q", "r", "s"], [["⇔", "r", "⇒", "p", "q"], ['⇔', 's', '∧', 'p', 'q']])
K = Agent(IC, {"p": 0, "q": 0, "r": 1, "s": 0})
K.models