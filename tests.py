from matrix import Matrix
import numpy as np

a = np.arange(12).reshape(3,4)
print(a)
print(a[1, 2])
m = Matrix((10, 10), [x for x in range(100)])
tests = [
    m,
    m[1,1],
    m[1],
    m[-1],
    m[1:4],
    m[:4],
    m[4:],
    m[:],
    m[1:7:2],
    m[:,1],
    m[1:4, 1:4],
    m[1:4, :4],
    m[1:4, 4:],
    m[1:4, :],
    m[-1:],
    m[-2::-2],
    m[-2::-2, 1:4],
    m[:, :],
    m[[1, 4]],
    m[:, [1,4]],
    m[[1,4], [1,4]]
]

i = 1
for test in tests:
    print(f"------------------------Test: {i}--------------------\n")
    i += 1
    print(test)