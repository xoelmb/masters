import random


def init_matrix(h, w):
    return [[random.choice([0,1]) for _ in range(w)] for _ in range(h)]


def next_state(state, neighbours):
    if (state == 1 and (neighbours == 2 or neighbours == 3)) or (state == 0 and neighbours == 3):
        return 1
    else:
        return 0


def count_neigh(matrix, i, j):
    count = 0
    for r in [-1, 0, 1]:
        if not r + i < 0 and r + i < len(field):
            for c in [-1, 0, 1]:
                if not c + j < 0 and c + j < len(field[0]):
                    if r != 0 or c != 0:
                        count += matrix[i + r][j + c]
    return count


def iterate(matrix):
    new_matrix = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            new_matrix[i][j] = next_state(matrix[i][j], count_neigh(matrix, i, j))
    if new_matrix == matrix:
        print("Warning: the simulation is stuck.")
    return new_matrix


def check_alive(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] != 0:
                return True
    return False


def print_field(matrix):
    print("+"+"-"*len(matrix[0])+"+")
    for line in matrix:
        print("|"+"".join(str(x) for x in line).replace("0", " ").replace("1", "X")+"|")
    print("+"+"-"*len(matrix[0])+"+")


field = init_matrix(10, 10)  # Initializes a random matrix of [0,1] values using given dimensions

while True:  # Runs the code below continuously until user stops it
    print_field(field)  # Prints the matrix
    if check_alive(field) == False:
        print("Extinction has occurred. Thanks for playing.\nExiting...")
        exit(0)
    print("Do you want to continue? (y/n)")  # Asks the user to continue the simulation
    answer = input()
    while answer != "n" and answer != "y":
        print("Please, enter a valid answer (y/n)\nDo you want to continue?")
        answer = input()
    if answer == "y":
        field = iterate(field)
    else:
        print("Thanks for playing!")
        exit(0)