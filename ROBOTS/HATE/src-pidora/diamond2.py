import numpy as np

def fillTheMap(myMap, maxSize, size):
    x, y, half = size // 2, size // 2, size // 2
    if (half < 1):
        return myMap
    for y in range(half, maxSize, size):
        for x in range(half, maxSize, size):
            squareStep(myMap, x, y, half, int(random.uniform(0, 1) * size * 0.3))

    for y in range(0, maxSize + 1, half):
        for x in range((y + half) % size, maxSize + 1, size):
            diamondStep(myMap, x, y, half, maxSize, int(random.uniform(0, 1) * size * 0.3))

    fillTheMap(myMap, maxSize, size // 2)


def squareStep(myMap, x, y, size, offset):
    myMap[x][y] = (myMap[x + size][y + size] + myMap[x - size][y + size] + myMap[x + size][y - size] + myMap[x - size][
        y - size]) // 4 + offset
    return myMap


def check(myMap, x, y, maxSize):
    if x < 0 or x > maxSize or y < 0 or y > maxSize:
        return -1
    else:
        return myMap[x][y]


def diamondStep(myMap, x, y, size, maxSize, offset):
    res = np.array([check(myMap, x, y + size, maxSize), check(myMap, x, y - size, maxSize),
                    check(myMap, x + size, y, maxSize), check(myMap, x - size, y, maxSize)])
    value, length = 0, 0
    for i in range(len(res)):
        if res[i] != -1:
            value += res[i]
            length += 1
    myMap[x][y] = value // length + offset
    return myMap