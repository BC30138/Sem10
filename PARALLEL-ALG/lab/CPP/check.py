import numpy as np

A = np.array([
    [0.850324, 3.98008, 0.0],
    [1.8969  , 7.43512, 5.11713],
    [0.0     , 8.09567, 9.95085]
    ])

d = np.array([8.91611, 5.6039, 9.66611])

print(np.linalg.solve(A, d))