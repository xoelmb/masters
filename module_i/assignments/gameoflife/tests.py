import random

init_field = [[round(random.randint(0, 3)) for _ in range(3)] for _ in range(4)]
for i in init_field:
    print(i)
# print(init_field[0])
# print(init_field[0][0])

for row in range(len(init_field)):
    print("\n\n", init_field[row])
    for column in range(len(init_field[row])):
        print("\n", init_field[row][column], "Neighbours:", end="")
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                try:
                    print(init_field[row+i][column+j], end="")
                except(IndexError):
                    pass