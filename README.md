# boolean-algebra
Python library for boolean algebra on arbitrary boolean sentences. Created towards my undergraduate thesis research at Pomona College in modeling social epistemology with dynamical systems.



# TODO:
1. test interpretations in belief base, now that they use List instead of Tuple
2. implement and test models_from_interpretation utils method
3. use models_from_interpretation method in GraphFromModels to call hamming_distance
4. hamming_distance will fail with exceptions when the input is not 0 or 1 (should I create a 'binary' enum type to handle this instead?)
5. tested BeliefBase methods should also handle invalid inputs (also with typing)
6. EXtract types to its own file
