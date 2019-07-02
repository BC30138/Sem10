import numpy as np

file = open("data/test_matrix.data")
lines = file.readlines() 
n = int(lines[0].rstrip().split()[1])
matrix = []
for line_it in range(5, 5 + n):
    matrix.append(list(map(float, lines[line_it].rstrip().split('\t')))) 

d = lines[5 + n].rstrip().split()
del d[0]
d = np.array(list(map(float, d)))
matrix = np.array(matrix)

print(np.linalg.solve(matrix, d))