# This script runs a Game of Life simulation for as long as the user wants (unless there's no more cells alive).
# I first used a while True loop to run the simulation, but this final version relays on recursion. I did this to have
# some extra practice on recursion and it was easy to apply to this scenario.
# Some of the loops that are used in the script are somehow redundant, but I purposely did so to gain modularity and
# to have short, well-defined functions.
# Even tough it was not needed, the script raises a warning if the simulation gets "stuck" (i.e. it does not change over
# iterations.

import random


def init_matrix(h, w):  # Creates a matrix of given dimensions containing only 0 or 1 randomly
    return [[random.choice([0, 1]) for _ in range(w)] for _ in range(h)]


def iterate(matrix):  # Runs the code below continuously until user stops it
    print_field(matrix)  # Prints the matrix
    if check_alive(matrix) is False:
        print("Extinction has occurred. Thanks for playing.\nExiting...")
        exit(0)
    print("Continue simulation (y/n)?", end="")  # Asks the user to continue the simulation
    answer = input()
    while answer != "n" and answer != "y":
        print("Please, enter a valid answer (y/n)\nContinue simulation (y/n)? ", end="")
        answer = input()
    if answer == "y":
        iterate(next_field(matrix))  # Recursively call the same function to keeo the simulation running
    else:
        print("Thanks for playing!")
        exit(0)


def print_field(matrix):  # Prints a 0/1 matrix as a field (" "/"X" and borders)
    print("+" + "-" * len(matrix[0]) + "+")
    for line in matrix:
        print("|" + "".join(str(x) for x in line).replace("0", " ").replace("1", "X") + "|")
    print("+" + "-" * len(matrix[0]) + "+")


def check_alive(matrix):  # Checks if there's any alive cells. Only returns 0 if all values in matrix are 0 (dead)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] != 0:
                return True
    return False


def next_field(matrix):  # Takes a matrix and returns the matrix of the next generation
    new_matrix = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]  # Initializes a 0 matrix
    for i in range(len(matrix)):  # Iterates over the rows
        for j in range(len(matrix[0])):  # Iterates over the columns of each row
            # Assign the state of a given cell in the next generation
            new_matrix[i][j] = next_state(matrix[i][j], count_neigh(matrix, i, j))
    if new_matrix == matrix:  # Checks is the simulation is stuck (no changes from previous generation)
        print("Warning: the simulation is stuck.")
    return new_matrix


def count_neigh(matrix, i, j):  # Computes the sum of the alive neighbours of a single cell
    count = 0
    for r in [-1, 0, 1]:  # Iterates the neighbour rows
        if not r + i < 0 and r + i < len(field):  # Checks that the row to be counted is in range
            for c in [-1, 0, 1]:  # Iterates over the neighbour columns
                if not c + j < 0 and c + j < len(field[0]):  # Checks that the column to be counted is in range
                    if r != 0 or c != 0:  # Checks that the cell to be counted is not the input cell itself
                        count += matrix[i + r][j + c]
    return count


def next_state(state, neighbours):  # Computes if the cell should be alive or dead in the next generation
    if (state == 1 and (neighbours == 2 or neighbours == 3)) or (state == 0 and neighbours == 3):
        return 1
    else:
        return 0


print("Welcome to the Game Of Life\n")
field = init_matrix(10, 10)  # Initializes a random matrix of [0,1] values using given dimensions
iterate(field)  # Starts running the simulation
