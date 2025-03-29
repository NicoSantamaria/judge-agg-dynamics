# judge-agg-dynamics
Python library for boolean algebra on arbitrary boolean sentences. Created towards my undergraduate thesis research at Pomona College in modeling social epistemology with dynamical systems.

# TODO
1. Error handling for wrong args numbers in use_operation
2. allow sentences to be input as chars or Prop types in Belief Base
3. test new input strategy in test_belief_base
4. start converting GraphFromModels to new enums and test

1. GraphFromModels -- why even call AgentFromModels? just take model
directly -- then can rename to Graph and delete AgentFromModels class
