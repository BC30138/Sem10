import numpy as np
g_top = 0.5
g_low = -0.5

def find_size(initial):
    for i in range(12):
        if 2 ** i + 1 >= initial:
            return 2 ** i + 1, i

def create_map(initial_size):
    size, depth = find_size(initial_size)
    map_h = 0 * np.ones((size, size))
    map_h[0][0] = np.random.rand()
    map_h[0][size-1] = np.random.rand()
    map_h[size - 1][0] = np.random.rand()
    map_h[size - 1][size - 1] = np.random.rand()
    # map_h[0][0] = 1
    # map_h[0][size-1] = 1
    # map_h[size - 1][0] = 1
    # map_h[size - 1][size - 1] = 1

    for i in range(depth + 1):
        for j in range(4 ** i):
            k = j // 2 ** i
            k *= size // 2 ** i
            j %= 2 ** i
            j *= size // 2 ** i
            if i == 0:
                sq_size = size
            else:
                sq_size = (size // 2 ** i) + 1
            # print("sq", j, k, sq_size)
            fill_square(map_h, j, k, sq_size, 2**i)
        for j in range(4 ** i):
            k = j // 2 ** i
            k *= size // 2 ** i
            j %= 2 ** i
            j *= size // 2 ** i
            if i == 0:
                sq_size = size
            else:
                sq_size = (size // 2 ** i) + 1
            # print("dmnd", j, k, sq_size)
            fill_diamond(map_h, j, k, sq_size, 2**i)


    return map_h[:initial_size,:initial_size]

def mean(lst):
    sum = 0
    count = 0
    for i in lst:
        if i != 0:
            sum += i
            count += 1
    # print(sum/count)
    return sum / count


def fill_square(map_h, position_x, position_y, size, delim):
    if size != 2:
        map_h[position_x + size // 2][position_y + size // 2] = mean([map_h[position_x][position_y],
                                                                 map_h[position_x][position_y + size - 1],
                                                                 map_h[position_x + size - 1][position_y],
                                                                 map_h[position_x + size - 1][position_y + size - 1]])+\
                                                                (np.random.uniform(low=g_low/delim, high=g_top/delim))


def fill_diamond(map_h, position_x, position_y, size, delim):
    if size != 2:
        temp = 0
        if position_x - size // 2 >= 0:
            temp = map_h[position_x - size // 2][position_y + size // 2]

        map_h[position_x][position_y + size // 2] = mean ([map_h[position_x][position_y],
                                                     map_h[position_x][position_y + size - 1],
                                                     map_h[position_x + size // 2][position_y + size // 2], temp])\
                                                    +(np.random.uniform(low=g_low/delim, high=g_top/delim))
        if position_y - size // 2 >= 0:
            temp = map_h[position_x + size // 2][position_y - size // 2]
        else: temp = 0

        map_h[position_x + size // 2][position_y] = mean ([map_h[position_x][position_y],
                                                     map_h[position_x + size - 1][position_y],
                                                     map_h[position_x + size // 2][position_y + size // 2], temp])\
                                                    + np.random.uniform(low=g_low/delim, high=g_top/delim)

        if position_y + size + size // 2 < len(map_h):
            temp = map_h[position_x + size // 2][position_y + size + size // 2 - 1]
        else: temp = 0

        map_h[position_x + size // 2][position_y + size - 1] = mean([map_h[position_x][position_y + size - 1],
                                                                map_h[position_x + size - 1][position_y + size - 1],
                                                                map_h[position_x + size // 2][position_y + size // 2],temp])\
                                                               + np.random.uniform(low=g_low/delim, high=g_top/delim)
        if position_x + size + size // 2 < len(map_h):
            temp = map_h[position_x + size + size // 2 - 1][position_y + size // 2]
        else: temp = 0
        map_h[position_x + size - 1][position_y + size // 2] = mean([map_h[position_x + size - 1][position_y],
                                                                map_h[position_x + size - 1][position_y + size - 1],
                                                                map_h[position_x + size // 2][position_y + size // 2], temp])\
                                                               + np.random.uniform(low=g_low/delim, high=g_top/delim)

