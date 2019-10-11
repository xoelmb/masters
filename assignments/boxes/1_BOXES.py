import sys


### 3 Función general para construir la parrilla de cajas cruzadas.

def build_boxes(box, grid):
    # 3.1 Comprueba si habrá que hacer una X:

    if box % 2 == 0:
        cross = False
    else:
        cross = True

    # 3.2 Hace el límite superior
    border_row(box, grid)

    # 3.3 Entrar a hacer cada fila de cajas
    for _ in range(0, grid):

        # 3.4 Entrar a hacer cada fila de cada fila de cajas excepto la final
        for j in range(1, box - 1):

            # 3.5 Comprueba si hay que hacer una X en esta línea:
            if cross == True and j == box // 2:
                middle_row(box, grid)

            # 3.6 El resto de casos, print una línea cualquiera diciéndole la posición de las barras laterales, que es el número de fila:
            else:
                any_row(box, grid, j)

        # 3.7 Imprime una línea de borde al acabar el interior de la fila de cajas.
        border_row(box, grid)


### 4 Función que imprime líneas límite entre cajas, iniciales y finales.
def border_row(box, grid):
    print("+", end="")

    # 4.1 Para cada caja de la fila, imprimimos los - necesarios con un + final.
    for i in range(0, grid):
        print("-" * (box - 2) + "+", end="")

    # 4.2 Cada vez que acabamos una fila, hacemos un salto de línea.
    print()


### 5 Función que imprime las líneas del interior excepto la media
def any_row(box, grid, pos):
    print("|", end="")

    # 5.1 Entramos en cada caja de la fila de cajas
    for i in range(0, grid):

        # 5.2 Entramos en la línea de la caja
        for j in range(1, box - 1):

            # 5.3 Escribe \ o / cuando corresponda. En el resto de casos, " ".
            if j == pos:
                print("\\", end="")
            elif j == box - pos - 1:
                print("/", end="")
            else:
                print(" ", end="")
        print("|", end="")
    print("")


### 6 Esta función escribe una X en las filas que corresponda.
def middle_row(box, grid):
    print("|", end="")
    for i in range(0, grid):
        for j in range(1, box - 1):
            if j == box // 2:
                print("X", end="")
            else:
                print(" ", end="")
        print("|", end="")
    print("")


# 1 Tomamos los parámetros como tamaño de la caja y de la cuadrícula, comprobando que las dimensiones sean suficientes para construir la cuadrícula.
box_size = int(sys.argv[1])
grid_size = int(sys.argv[2])

if box_size < 2:
    print("Box dimensions are too small.")
    exit()

if grid_size < 1:
    print("Grid size must be 1 at least.")
    exit()

# 2 Construimos la cuadrícula con la función definida anteriormente.
build_boxes(box_size, grid_size)
