from Agent import Agent
from BeliefBase import BeliefBase
from Graph import Graph

if __name__ == "__main__":
    agenda = BeliefBase(["p", "q", "r", "s"])
    agenda.add_constraint(["⇔", "r", "⇒", "p", "q"])
    agenda.get_models()
    
    print(K.models)