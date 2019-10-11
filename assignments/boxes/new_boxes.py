import sys


def build_boxes(box, grid):  # Main function to elaborate the boxes
    border_row(box, grid)  # Prints first row

    for _ in range(grid):  # Loop repeated as many times as rows of boxes needed
        for i in range(1, box - 1):  # Loop to access each row inside a given row of boxes
            inside_row(box, grid, i)  # Prints the row

        border_row(box, grid)  # Prints a border row after the inside of the box


def border_row(box, grid):  # Prints a border row (top, bottom and box-connecting rows)
    print("+", end="")  # Prints first character of the row

    for _ in range(grid):  # Loop repeated as many times as boxes in a row
        print("-" * (box - 2) + "+", end="")  # Prints the rest of the row

    print()  # Prints an end of line


def inside_row(box, grid, position):  # Prints the rows inside the boxes
    print("|", end="")  # Starts the line with this character

    for _ in range(grid):  # Repeats a loop as many times as boxes in one line
        for j in range(1, box - 1):  # Repeats loop as many times as positions inside one box

            if j == box // 2 and j == position and box % 2 != 0:  # Checks if an X is needed at that position
                print("X", end="")

            elif j == position:  # Checks if \ is needed
                print("\\", end="")

            elif j == box - 1 - position:  # Checks if / is needed
                print("/", end="")

            else:  # If nothing special is needed, then prints a blank space
                print(" ", end="")

        print("|", end="")  # Prints | at the limit of each box

    print()  # Prints an end-of-line


try:
    box_size = int(sys.argv[1])  # Takes box size
    grid_size = int(sys.argv[2])  # Takes grid size

except:
    print("You need to provide two numbers to build the grid.")

if box_size < 2:  # Checks if box dimensions are big enough
    print("Box dimensions are too small.")
    exit()

if grid_size < 1:  # Checks if grid dimensions are valid
    print("Grid size must be 1 at least.")
    exit()

build_boxes(box_size, grid_size)  # Uses the previously defined function to print the boxes
