import random


def init_matrix(h, w):
    return [[round(random.randint(0, 1)) for _ in range(w)] for _ in range(h)]


field = init_matrix(3,4)
for i in field:
    print(i)

# for i in range(len(field)):
#     for j in range(len(field[0])):
#         print(field[i][j], end="")
#     print()

for i in range(len(field)):
    for j in range(len(field[0])):
        n=1
        print(i, j, ":", field[i][j], ":")
        for r in [-1,0,1]:
            if not r+i < 0 and r+i < len(field):
                for c in [-1, 0,1]:
                    if not c+j < 0 and c+j < len(field[0]):
                        if r != 0 or c != 0:
                            print("({})".format(n),str(r+i),str(j+c),":",field[i+r][j+c], end="   ")
                            n+=1
        print()