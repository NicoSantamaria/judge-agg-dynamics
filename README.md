# judge-agg-dynamics
Python library for boolean algebra on arbitrary boolean sentences. Created towards my undergraduate thesis research at Pomona College in modeling social epistemology with dynamical systems.

# TODO
1. Error handling for wrong args numbers in use_operation
2. allow sentences to be input as chars or Prop types

1. extract logic oeprations to utils.py
2. use __call__ to cover error handling for Logic and Prop enums
3. make sure all tests pass for Logic and Prop types
4. Implement utils.py function to translate from "p" -> Prop.P and etc.,
so that inputs are less verbose
