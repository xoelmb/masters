import random


def init_matrix(h, w):
    return [[round(random.randint(0, 1)) for _ in range(w)] for _ in range(h)]


def count_neigh(matrix, i, j):
    print("contando", i, j)
    count = 0
    for row in [-1,0,1]:
        for column in [-1,0,1]:
            if i != row and j != column:
                try:
                    count += matrix[i+row][j+column]
                except:
                    count += 0
    print(count)
    return count


def next(matrix):
    new_matrix = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    for row in range(len(matrix)):
        for column in range(len(matrix[0])):
            count = count_neigh(matrix, row, column)
            new_matrix[row][column] = count
    return new_matrix


field = init_matrix(3,4)
for i in field:
    print(i)

field_count = next(field)
for i in field_count:
    print(i)