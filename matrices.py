import numpy as np
from functools import reduce

a = np.array([[1,0,1/3],
              [0,1/2,1/3],
              [0,1/2,1/3]])

eigenvalues, trans_matrix = np.linalg.eig(a)
diagonal = np.diag(eigenvalues)
trans_matrix_inv = np.linalg.inv(trans_matrix)

first = np.linalg.matrix_power(a, 1000)
second = reduce(np.matmul, [trans_matrix, np.linalg.matrix_power(diagonal, 1000), trans_matrix_inv])

print(first)
print(second)

# it works!