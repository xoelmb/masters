import copy

sudoku = [
    [5, "?", "?", "?", 8, "?", "?", 4, 9],
    ["?", "?", "?", 5, "?", "?", "?", 3, "?"],
    ["?", 6, 7, 3, "?", "?", "?", "?", 1],
    [1, 5, "?", "?", "?", "?", "?", "?", "?"],
    ["?", "?", "?", 2, "?", 8, "?", "?", "?"],
    ["?", "?", "?", "?", "?", "?", "?", 1, 8],
    [7, "?", "?", "?", "?", 4, 1, 5, "?"],
    ["?", 3, "?", "?", "?", 2, "?", "?", "?"],
    [4, 9, "?", "?", 5, "?", "?", "?", 3]]


def solve_sudoku(sudoku, x, y):
    if y == 9:
        print_sudoku(sudoku)
    else:
        if x == 8:
            x_next = 0
            y_next = y + 1
        else:
            x_next = x + 1
            y_next = y

        if sudoku[x][y] != "?":
            solve_sudoku(sudoku, x_next, y_next)
        else:
            sudoku_next = copy.deepcopy(sudoku)
            for n in range(1, 10):
                sudoku_next[x][y] = n
                if valid_sudoku(sudoku_next):
                    solve_sudoku(sudoku_next, x_next, y_next)


def valid_sudoku(sudoku):
    # Check rows
    for x in range(0, 9):
        components = []
        for y in range(0, 9):
            components.append(sudoku[x][y])
        if not valid_component(components):
            return False
    # Check columns
    for y in range(0, 9):
        components = []
        for x in range(0, 9):
            components.append(sudoku[x][y])
        if not valid_component(components):
            return False
    # Check small squares
    for n1 in [0, 3, 6]:
        for n2 in [0, 3, 6]:
            components = []
            for x in range(n1, n1 + 3):
                for y in range(n2, n2 + 3):
                    components.append(sudoku[x][y])
            if not valid_component(components):
                return False
    # All OK
    return True


def valid_component(components):
    occurs = [False for _ in range(0, 9)]
    for n in components:
        # Check unknown
        if n == "?": continue
        # Check repeated
        if occurs[n - 1]: return False
        # Annotate
        occurs[n - 1] = True
    # All OK
    return True


def print_sudoku(sudoku):
    for i in sudoku:
        print(i)
    print()

solve_sudoku(sudoku, 0 , 0)