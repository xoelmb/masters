########################################################################################################################
#################                                    ALGORITHMS 1                                    ###################
########################################################################################################################

# BLOCK EXERCISES

# Lo importante es sacar la fórmula de la complejidad (lineal, logarítmica o lo que sea). Luego es sustituir los valores
# para hallar C, y podemos aplicar el dato que nos pide.

# [E0] Compute the complexity of the following algorithms. Taking into
# account that it has taken 50s to run for n=1000, calculate how long it
# will take to run for n=100000.
import copy


def sum_list(my_list):
    count = 0
    for elm in my_list:
        count += elm
    return count


# lineal: ejecuta una orden por cada elemento de la lista: O(n) = n


# [E1] Compute the complexity of the following algorithms. Taking into
# account that it has taken 60s to run for n=140, calculate how long it
# will take to run for n=500.


def factorial(n):
    result = n
    for i in range(1, n):
        result *= i
    return result


# lineal: ejecuta una orden por cada elemento hasta n: O(n) = n


# [E2] Compute the complexity of the following algorithms. Taking into
# account that it has taken 40s to run for n=10, calculate how long it
# will take to run for n=1000.


def remove_adaptor_list(sequence, adaptor_list):
    for adaptor in adaptor_list:
        if sequence[0:len(adaptor)] == adaptor:
            return sequence[len(adaptor):]
    return sequence


# exponencial: el loop se ejecuta n veces (cantidad de adaptadores), y cada vez tiene que hacer m comprobaciones (carac-
# teres que tenga el adaptor). O(n*len(adaptor))


# [E3] Compute the complexity of the following algorithms. Taking into
# account that it has taken 90s to run for n=100, calculate how long it
# will take to run for n=200.


def reverse(sequence):
    sequence_rev = ""
    for i in range(1, len(sequence) + 1):
        sequence_rev += sequence[len(sequence) - i]
    return sequence_rev


# lineal: siendo n la cantidad de caracteres, tiene que ejecutar n órdendes: O(n) = n

# [E4] Compute the complexity of the following algorithms. Taking into
# account that it has taken 30s to run for n=10, calculate how long it
# will take to run for n=100.


def reverse_complement(dna):
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    return ''.join([complement[base] for base in dna[::-1]])


# lineal: un join por cada caracter que hay en la secuencia


# [E5] Compute the complexity of the following algorithms. Taking into
# account that it has taken 33s to run for n=100, calculate how long it
# will take to run for n=1000.


def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n - 1)


# lineal, porque solo hace una multiplicación y una comprobación por cada número hasta n

# [E6] Compute the complexity of the following algorithms. Taking into
# account that it has taken 4s to run for n=1000, calculate how long it
# will take to run for n=2000.


def binarysearch(sequence, value):
    lo, hi = 0, len(sequence) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if sequence[mid] < value:
            lo = mid + 1
        elif value < sequence[mid]:
            hi = mid - 1
        else:
            return mid
    return None


# logarítmico: ángel dice que base log2, las soluciones ponen solo log, pero tiene sentido base 2. O(log(n))


# [E7] Compute the complexity of the following algorithms. Taking into
# account that it has taken 4s to run for n=1000, calculate how long it
# will take to run for n=2000.


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


# Exponencial: 2^n porque ejecuta dos operaciones por cada número que hay hasta n

########################################################################################################################
#################                                    ALGORITHMS 2                                    ###################
########################################################################################################################

# 1. Divide and conquer: intuition
# Searching a number in a list


def search(numbers, n):
    for x in numbers:
        if x == n:
            return True
    return False


# Searching a number in a list. Recursively & DAC:


# Breve explicación del DAC con el siguiente ejercicio.
# Excepto la última vez, entras siempre en el else, que te divide la lista, y entra en la función, en el else otra vez,
# que divide la lista, y entra en la función... total, que te irá haciendo dos listas más pequeñas por cada paso. Al fi
# nal te quedas con muchas listas que se habrán quedado con 1 o 0 elementos. Cuando son de 0 elemento, en esa lista obv
# iamente no está el valor que estás buscando, así que devuelve false. En las que haya quedado 1 elemento, comprobará si
# es el valor n que estás buscando. Si lo es, devuelve True, y al devolver True, esa lista returnea True a la función
# que la llamó, y esta, al cumplirse el if donde la llama, returnea True a la que la llamó, y el True va "ascendiendo"
# en las llamadas de funciones hasta que devuelve True a la original. Si ninguna lista de 1 elemento devuelve True,
# llegas a la orden return False del final.


def search(numbers, n):
    if len(numbers) == 0:
        return False
    elif len(numbers) == 1:
        return numbers[0] == n
    else:
        middle = len(numbers) // 2
        if (search(numbers[0:middle], n)): return True
        if (search(numbers[middle:], n)): return True
        return False


# Searching a number in a sorted list
# Lo mismo, pero solo llamando a la recursión de la mitad de la lista que puede contener el elemento.

def search(numbers, n):
    if len(numbers) == 0:
        return False
    elif len(numbers) == 1:
        return numbers[0] == n
    else:
        middle = len(numbers) // 2
        if n < numbers[middle]:
            return search(numbers[0:middle], n)
        else:
            return search(numbers[middle:], n)


# 2. Comparing VCF records

# Primero comprueba el campo cromosoma, y si son iguales, el de posición.
def compare_vcf(vcf1, vcf2):
    if vcf1[0] < vcf2[0]:
        return -1
    elif vcf1[0] > vcf2[0]:
        return 1
    else:
        if vcf1[1] < vcf2[1]:
            return -1
        elif vcf1[1] > vcf2[1]:
            return 1
        else:
            return 0


# Prints "0"
print(compare_vcf(("Chr1", 45798901, "GTGTGT", ""), ("Chr1", 45798901, "C", "T")))
# Prints "-1"
print(compare_vcf(("Chr1", 45798901, "C", "T"), ("Chr2", 793301, "GTGTGT", "")))
# Prints "1"
print(compare_vcf(("Chr2", 793301, "GTGTGT", ""), ("Chr1", 45798901, "C", "T")))


# 2. Searching for a variant

# Te comprueba si un record vcf que le pases está contenido en una lista de records vcf, y te devuelve el índice.

def search_vcf_list(nlist, number):
    idx = 0
    for i in nlist:
        if number == i:
            return idx
        idx += 1
    return -1


list_vcf = [("ChrX", 100, "C", "T"), ("Chr1", 50, "", "T"), ("Chr2", 200, "C", ""), ("Chr1", 100, "T", "G"),
            ("Chr3", 40, "CCC", "")]
# Prints "3"
print(search_vcf_list(list_vcf, ("Chr1", 100, "T", "G")))
# Prints "-1"
print(search_vcf_list(list_vcf, ("ChrY", 10, "", "GTG")))


# 2. Searching for a variant. Binary search


def binary_search_vcf_list(vcf_list, vcf):
    first = 0
    last = len(vcf_list) - 1
    while first <= last:
        midpoint = (first + last) // 2
        if compare_vcf(vcf_list[midpoint], vcf) == 0:
            return midpoint
        elif compare_vcf(vcf, vcf_list[midpoint]) == -1:
            last = midpoint - 1  # First half
        else:
            first = midpoint + 1  # Second half
    return -1


# 3. Sort two VCF records

# Usa la función de antes para comparar dos vcf y te los devuelve ordenados

def sort_2vcf(vcf1, vcf2):
    if compare_vcf(vcf1, vcf2) <= 0:
        return [vcf1, vcf2]
    else:
        return [vcf2, vcf1]


# Prints "[('Chr1', 45798901, 'C', 'T'), ('Chr2', 793301, 'GTGTGT', '')]"
print(sort_2vcf(("Chr2", 793301, "GTGTGT", ""), ("Chr1", 45798901, "C", "T")))
# Prints "[('Chr1', 45798901, 'C', 'T'), ('Chr2', 793301, 'GTGTGT', '')]"
print(sort_2vcf(("Chr1", 45798901, "C", "T"), ("Chr2", 793301, "GTGTGT", "")))


# 3. Merge two lists of sorted VCF records

# teniendo dos listas ordenadas, te las junta también dando una lista ordenada. Lo que hace es coger el elemento más pe-
# queño de la primera lista y compararlo con el más pequeño de la segunda (LOS MÁS PEQUES SON LOS PRIMEROS PORQUE ESTÁN
# ORDENADAS). Añade entonces el más pequeño a la lista merged y suma uno al pointer de esa lista para la siguiente vez
# comprobar el siguiente elemento. Cuando has acabado con una de las listas, añade lo que queda de la otra a la lista
# merged


def merge_vcf_lists(list1, list2, merged):
    p1 = 0
    p2 = 0
    pmerged = 0
    # Merge both list by comparing each element at the head
    while p1 < len(list1) and p2 < len(list2):
        if compare_vcf(list1[p1], list2[p2]) <= 0:
            merged[pmerged] = list1[p1]
            p1 += 1
        else:
            merged[pmerged] = list2[p2]
            p2 += 1
        pmerged += 1
    # Append the remaining elements of list1
    while p1 < len(list1):
        merged[pmerged] = list1[p1]
        p1 += 1
        pmerged += 1
    # Append the remaining elements of list2
    while p2 < len(list2):
        merged[pmerged] = list2[p2]
        p2 += 1
        pmerged += 1


# Sample data
list1 = [("Chr1", 100, "C", "T"), ("Chr3", 20, "C", "T")]
list2 = [("Chr1", 900, "C", "T")]
merged = [0] * (len(list1) + len(list2))  # Declare empty list
# Merge list of VCF records
merge_vcf_lists(list1, list2, merged)
# Prints "[('Chr1', 100, 'C', 'T'), ('Chr1', 900, 'C', 'T'), ('Chr3', 20, 'C', 'T')]"
print(merged)


# 3. VCF MergeSort

# DAC. Vas a entrar en el else las primeras veces. En el else, divides la lista en dos, izq y der, y las pasas a la fun-
# ción de nuevo. Entras en el else y bueno, así hasta que las listas solo tienen un elemento! Cuando tienen un elemento
# y se la pasas a la función, te devuelve un return sin nada, que para la recursión, es decir, la función que pasó esa
# lista de un elemento puede continuar la siguiente línea, que es merge_vcf_lists, que lo que hace es devolverte una lis
# ta ordenada de las dos anteriores.

def merge_sort_vcf_lists(vcf_list):
    # Check list length
    if len(vcf_list) == 1:
        return
    else:
        middle_point = len(vcf_list) // 2
        left_list = vcf_list[:middle_point]  # Left-half of the list
        right_list = vcf_list[middle_point:]  # Right-half of the list
        # Sort recursively the halves
        merge_sort_vcf_lists(left_list)
        merge_sort_vcf_lists(right_list)
        # Merge both halves into the final sorted list
        merge_vcf_lists(left_list, right_list, vcf_list)


list_vcf = [("ChrX", 100, "C", "T"),
            ("Chr1", 50, "", "T"),
            ("Chr2", 200, "C", ""),
            ("Chr1", 100, "T", "G"),
            ("Chr3", 40, "CCC", "")]
# Merge sort
merge_sort_vcf_lists(list_vcf)
# [('Chr1', 50, '', 'T'),
# ('Chr1', 100, 'T', 'G'),
# ('Chr2', 200, 'C', ''),
# ('Chr3', 40, 'CCC', ''),
# ('ChrX', 100, 'C', 'T')]
print(list_vcf)


# 3. Sorting integers. MergeSort

# Son los mismos principios que los explicados para vcf que era más complicado.

def merge_lists(list1, list2, merged):
    p1 = 0
    p2 = 0
    pmerged = 0
    # Merge both list by comparing each element at the head
    while p1 < len(list1) and p2 < len(list2):
        if list1[p1] <= list2[p2]:
            merged[pmerged] = list1[p1]
            p1 += 1
        else:
            merged[pmerged] = list2[p2]
            p2 += 1
        pmerged += 1
    # Append the remaining elements of list1
    while p1 < len(list1):
        merged[pmerged] = list1[p1]
        p1 += 1
        pmerged += 1
    # Append the remaining elements of list2
    while p2 < len(list2):
        merged[pmerged] = list2[p2]
        p2 += 1
        pmerged += 1


def merge_sort(numbers_list):
    # Check list length
    if len(numbers_list) == 1:
        return
    else:
        middle_point = len(numbers_list) // 2
        left_list = numbers_list[:middle_point]  # Left-half of the list
        right_list = numbers_list[middle_point:]  # Right-half of the list
        # Sort recursively the halves
        merge_sort(left_list)
        merge_sort(right_list)
        # Merge both halves into the final sorted list
        merge_lists(left_list, right_list, numbers_list)


l = [3, 13, 16, 34, 2, 26, 43, 90, 55, 2, 2]
merge_sort(l)
print(l)


# 4. Challenge. My implementation from stackexchange.


def merge_sort(numbers_list):
    # Checking that the length of the (split) list is grater than 1
    if len(numbers_list) > 1:
        # Calculate the middle point
        t = len(numbers_list) // 2
        # Dividing the list of numbers, recursively pass it to merge_sort and making it iterable
        # Instead of using pointers, iterate using iter/next
        left_list = iter(merge_sort(numbers_list[:t]))
        n1 = next(left_list)
        right_list = iter(merge_sort(numbers_list[t:]))
        n2 = next(right_list)
        # Define the ordered list as an empty list
        numbers_list = []
        # Try will expand the list and iterate using next. When one of the list has been finished, it raises an error
        # so the except is called.
        try:
            while True:
                if n1 <= n2:
                    numbers_list.append(n1)
                    n1 = next(left_list)
                else:
                    numbers_list.append(n2)
                    n2 = next(right_list)
        # Except checks which of the list has been completed, and appends the other one with append/extend.
        except:
            if n1 <= n2:
                numbers_list.append(n2)
                numbers_list.extend(right_list)
            else:
                numbers_list.append(n1)
                numbers_list.extend(left_list)
    return numbers_list


# [E1] Implement a function that sorts a list of kmers (i.e. strings).

def sort_kmers(kmers_list):
    # Check list length
    if len(kmers_list) == 1:
        return
    else:
        middle_point = len(kmers_list) // 2
        left_list = kmers_list[:middle_point]
        right_list = kmers_list[middle_point:]
        # Sort recursively the halves
        sort_kmers(left_list)
        sort_kmers(right_list)
        # Merge both halves into the final sorted list
        merge_lists(left_list, right_list, kmers_list)


def merge_lists(list1, list2, merged):
    p1 = 0
    p2 = 0
    pmerged = 0
    # Merge both lists
    while p1 < len(list1) and p2 < len(list2):
        if list1[p1] <= list2[p2]:
            merged[pmerged] = list1[p1]
            p1 += 1
        else:
            merged[pmerged] = list2[p2]
            p2 += 1
        pmerged += 1
    # Append the remaining elements of list1
    while p1 < len(list1):
        merged[pmerged] = list1[p1]
        p1 += 1
        pmerged += 1
    # Append the remaining elements of list2
    while p2 < len(list2):
        merged[pmerged] = list2[p2]
        p2 += 1
        pmerged += 1


# Kmers
kmers = ["CGT", "TAG", "AAA"]
# Sort kmers
sort_kmers(kmers)
# Prints "["AAA","CGT","TAG"]"
print(kmers)


# [E2] Implement a function that binary searches a kmer within a
# sorted list of kmers
def binary_search(kmers_list, kmer):
    first = 0
    last = len(kmers_list) - 1
    while first <= last:
        midpoint = (first + last) // 2
        if kmers_list[midpoint] == kmer:
            return midpoint
        elif kmers_list[midpoint] > kmer:
            last = midpoint - 1
        else:
            first = midpoint + 1
    return -1


kmers = ['AAA', 'ACGT', 'CGT', 'CGTACG', 'GGTC', 'TAG']
print(binary_search(kmers, 'GGTC'))  # Prints 4
print(binary_search(kmers, 'A'))  # Prints -1
print(binary_search(kmers, 'TTTTTTT'))  # Prints -1
print(binary_search(kmers, 'AAA'))  # Prints 0
print(binary_search(kmers, 'TAG'))  # Prints 5


# Recursive implementation of the previous exercise.
def binary_search(kmers_list, kmer):
    if len(kmers_list) == 0:
        return -1
    elif len(kmers_list) == 1:
        return kmer == kmers_list[0]
    else:
        midpoint = len(kmers_list) // 2
        if kmer < kmers_list[midpoint]:
            return binary_search(kmers_list[:midpoint], kmer)
        else:
            return binary_search(kmers_list[midpoint:], kmer)


kmers = ['AAA', 'ACGT', 'CGT', 'CGTACG', 'GGTC', 'TAG']
print(binary_search(kmers, 'GGTC'))  # Prints True
print(binary_search(kmers, 'A'))  # Prints False
print(binary_search(kmers, 'TTTTTTT'))  # Prints False
print(binary_search(kmers, 'AAA'))  # Prints True
print(binary_search(kmers, 'TAG'))  # Prints True


# [E3] Given 3 sorted lists of kmers, implement a function that
# produces the merged sorted list of the three.
def merge_threeway(list1, list2, list3, merged):
    pmerged = 0
    p1, next_l1 = 0, -1
    p2, next_l2 = 0, -1
    p3, next_l3 = 0, -1
    if len(list1) > 0: next_l1 = list1[0]
    if len(list2) > 0: next_l2 = list2[0]
    if len(list3) > 0: next_l3 = list3[0]
    # Merge lists
    while p1 < len(list1) or p2 < len(list2) or p3 < len(list3):
        if next_l1 != -1 and (next_l2 == -1 or next_l1 <= next_l2) and (next_l3 == -1 or next_l1 <= next_l3):
            merged[pmerged] = list1[p1]
            p1 += 1
            next_l1 = list1[p1] if p1 < len(list1) else -1
        elif next_l2 != -1 and (next_l1 == -1 or next_l2 <= next_l1) and (next_l3 == -1 or next_l2 <= next_l3):
            merged[pmerged] = list2[p2]
            p2 += 1
            next_l2 = list2[p2] if p2 < len(list2) else -1
        else:
            merged[pmerged] = list3[p3]
            p3 += 1
            next_l3 = list3[p3] if p3 < len(list3) else -1
        pmerged += 1


# Recursive implementation
def merge_threeway(list1, list2, list3):
    # Compose list with leading elements
    head_elements = list()
    if len(list1) > 0: head_elements.append((list1[0], 0))
    if len(list2) > 0: head_elements.append((list2[0], 1))
    if len(list3) > 0: head_elements.append((list3[0], 2))
    # Check list length
    if len(head_elements) == 0: return []
    # Select minimum and merge
    minimun = min(head_elements)
    if minimun[1] == 0:
        return [minimun[0]] + merge_threeway(list1[1:], list2, list3)
    elif minimun[1] == 1:
        return [minimun[0]] + merge_threeway(list1, list2[1:], list3)
    elif minimun[1] == 2:
        return [minimun[0]] + merge_threeway(list1, list2, list3[1:])


list1 = ["AAA", "CGT", "TAG"]
list2 = ["CGT", "GGT"]
list3 = ["AA"]
merged = merge_threeway(list1, list2, list3)
print(merged)  # ['AA', 'AAA', 'CGT', 'CGT', 'GGT', 'TAG']


# [E4] Given a list of sorted lists of kmers, implement a function that
# produces the resulting merged sorted list of all.
def merge_lists(list1,list2):
    p1, p2 = 0, 0
    merged = list()
    # Merge both lists
    while p1 < len(list1) and p2 < len(list2):
        if list1[p1] <= list2[p2]:
            merged.append(list1[p1]); p1 += 1
        else:
            merged.append(list2[p2]); p2 += 1
    # Append the remaining elements of list1
    while p1 < len(list1):
        merged.append(list1[p1]); p1 += 1
    # Append the remaining elements of list2
    while p2 < len(list2):
        merged.append(list2[p2]); p2 += 1
    # Return
    return merged


def merge_nlists(nlist):
    def merge_nlists_rec(merged,nlist):
        if len(nlist) == 0:
            return merged
        else:
            return merge_nlists_rec(merge_lists(merged,nlist[0]),nlist[1:])
    return merge_nlists_rec([],nlist)


kmer_lists = [["AAA","CGT","TAG"],["CGT","GGT"],["AA"]]
merged = merge_nlists(kmer_lists)
print(merged) # ['AA', 'AAA', 'CGT', 'CGT', 'GGT', 'TAG']

# [E5] Given a sorted list of integers, implement a ternary search that,
# in the spirit of the binary search, divides the search space by 3 on
# each step of the search
def ternary_search(nlist,number):
    first = 0
    last = len(nlist) - 1
    while first <= last:
        step = (last-first) // 3
        centinel1 = first + step
        centinel2 = centinel1 + step
        # Check first third
        if number < nlist[centinel1]:
            last = centinel1 - 1
        elif number == nlist[centinel1]: return centinel1
        # Check second third
        elif number < nlist[centinel2]:
            first = centinel1 + 1
            last = centinel2 - 1
        elif nlist[centinel2] == number: return centinel2
        # Check third third
        else:
            first = centinel2 + 1
    return -1


numbers = [1,2,5,12,34,55,67,234,444]
print(ternary_search(numbers,12)) # Prints 3
print(ternary_search(numbers,2)) # Prints 1
print(ternary_search(numbers,0)) # Prints -1
print(ternary_search(numbers,999)) # Prints -1
print(ternary_search(numbers,1)) # Prints 0
print(ternary_search(numbers,444)) # Prints 8

########################################################################################################################
#################                                    ALGORITHMS 4                                    ###################
########################################################################################################################

# 1. Constrained K-mer generation: For a given k, generate all k-mers, that don’t contain any “GC” repetition

# A ver, aquí tienes la longitud k de tus kmers para empezar. como no es 0, entras en el else, que por cada letra te
# llama una vez a la función, pero con k-1, y diciéndo qué base es la que estás escribiendo. Entonces, lo que haces es
# ir llamando a la función con una k cada vez más pequeña y un kmer creado cada vez más largo! Cuando k = 0, has acabado
# de crear el kmer, y entonces se comprueba que no haya GC en el kmer creado antes de imprimirlo.
def enumerate_kmers_no_GC(k, base):
    if k == 0:
        if "GC" not in base:
            print(base)
    else:
        for c in "ACGT":
            enumerate_kmers_no_GC(k - 1, base + c)


# Generate all combinations
enumerate_kmers_no_GC(3, "")

# 2. Solving a maze.
import copy


def search_maze(maze, position, end):
    # Mark path with "*"
    v = position[0]
    h = position[1]
    maze[v][h] = "*"
    # Check position
    if position == end:
        print_maze(maze)
        return
    else:
        if v > 0 and maze[v - 1][h] == " ":
            maze_next = copy.deepcopy(maze)
            search_maze(maze_next, (v - 1, h), end)
        if v + 1 < len(maze) and maze[v + 1][h] == " ":
            maze_next = copy.deepcopy(maze)
            search_maze(maze_next, (v + 1, h), end)
        if h > 0 and maze[v][h - 1] == " ":
            maze_next = copy.deepcopy(maze)
            search_maze(maze_next, (v, h - 1), end)
        if h + 1 < len(maze[v]) and maze[v][h + 1] == " ":
            maze_next = copy.deepcopy(maze)
            search_maze(maze_next, (v, h + 1), end)


def print_maze(maze):
    for line in maze:
        print("".join(line))


maze = [
    list("----------------------------"),
    list("|  XXXX X  XX  XXX   XX  XX|"),
    list("|X XXXX X XX X  X  XXXX X X|"),
    list("|X XX    X X XX XXXX   XXX |"),
    list("|X XX X X XX X  X  X X XX X|"),
    list("|   X X XXX     XX X X  X X|"),
    list("| X X X X X X X XX   XX XXX|"),
    list("|XX   X   X X XXX  XXXX X  |"),
    list("| X X X XXX X XXX XXXXX XXX|"),
    list("|X  X X     X     XX       |"),
    list("----------------------------")]
start = (1, 1)
end = (9, 26)
# Search in the maze
search_maze(maze, start, end)


# 3. Sequence profile: Given a sequence and a k-mer length, compute the profile (or
# histogram) with the frequencies of each k-mer appearing in the sequence.


def kmer_profile(sequence, k):
    profile = {}
    for i in range(0, len(sequence) - k + 1):
        kmer = sequence[i:i + k]
        if kmer not in profile:
            profile[kmer] = 0
        profile[kmer] += 1
    return profile


# Declare sequence and k-mer length
sequence = "ACAGACTACGACTACGACGGAAACTG"
k = 2


# 4. Solving a sudoku.


def solve_sudoku(sudoku, x, y):
    # Check sudoku solved
    if y == 9:
        print_sudoku(sudoku)
    else:
        # Compute next position
        if x == 8:
            x_next = 0
            y_next = y + 1
        else:
            x_next = x + 1
            y_next = y
        # Check next position and solve
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
        if occurs[n - 1] == True: return False
        # Annotate
        occurs[n - 1] = True
    # All OK
    return True


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

solve_sudoku(sudoku, 0, 0)


########################################################################################################################
#################                                    ALGORITHMS 5                                    ###################
########################################################################################################################

# 2. Edit Distance. Brute Force:


def edit_distance(pattern, text):
    if len(pattern) == 0:
        # Insert all remaining chars
        return len(text)
    elif len(text) == 0:
        # Delete all remaining chars
        return len(pattern)
    else:
        # Find score for match/subtitution
        if pattern[0] == text[0]:
            m_cost = edit_distance(pattern[1:], text[1:])
        else:
            m_cost = edit_distance(pattern[1:], text[1:]) + 1
        # Find score for insertion
        i_cost = edit_distance(pattern[:], text[1:]) + 1
        # Find score for deletion
        d_cost = edit_distance(pattern[1:], text[:]) + 1
        # Find the minimum combination
        return min(m_cost, i_cost, d_cost)


pattern = "TAC"
text = "TC"
distance = edit_distance(pattern, text)
print(distance)  # Prints "1"


# 2. Edit Distance. Brute Force. Exercise: Implement the function edit distance that computes the
# actual set of edit operations that lead to the minimum distance


def edit_distance(pattern, text):
    if len(pattern) == 0:
        return (len(text), ["I"] * len(text))
    elif len(text) == 0:
        return (len(pattern), ["D"] * len(pattern))
    else:
        (m_cost, m_cigar) = edit_distance(pattern[1:], text[1:])
        (i_cost, i_cigar) = edit_distance(pattern[:], text[1:])
        (d_cost, d_cigar) = edit_distance(pattern[1:], text[:])
        minimum = min(m_cost, i_cost, d_cost)
        if minimum == m_cost:
            if (pattern[0] == text[0]):
                return (m_cost, ["M"] + m_cigar)
            else:
                return (m_cost + 1, ["X"] + m_cigar)
        elif minimum == i_cost:
            return (i_cost + 1, ["I"] + i_cigar)
        else:
            return (d_cost + 1, ["D"] + d_cigar)


# 2. Edit Distance. Pretty Print. Exercise: Given 2 sequence and a list of alignment operations (i.e.
# alignment cigar), print formatted the alignment between the pattern and the text.


def pretty_print_alignment(pattern, text, cigar):
    (pattern_txt, i) = ("", 0)
    operation_txt = ""
    (text_txt, j) = ("", 0)
    for op in cigar:
        if op == "M":
            pattern_txt += pattern[i]
            i += 1
            operation_txt += "/"
            text_txt += text[j]
            j += 1
        elif op == "X":
            pattern_txt += pattern[i]
            i += 1
            operation_txt += " "
            text_txt += text[j]
            j += 1
        elif op == "I":
            pattern_txt += " "
            operation_txt += " "
            text_txt += text[j]
            j += 1
        elif op == "D":
            pattern_txt += pattern[i]
            i += 1
            operation_txt += " "
            text_txt += " "

    print(pattern_txt)
    print(operation_txt)
    print(text_txt)


# Compute edit distance
(distance, cigar) = edit_distance("GATTACA", "GGACTCA")
# Prints "(2, ['I', 'M', 'M', 'M', 'M', 'D', 'M', 'M'])"
print(distance, cigar)
# Prints Pretty
pretty_print_alignment("GATTACA", "GGACTCA", cigar)


# GATTACA
# || | ||
# GGACT CA


# 3. Dynamic Programming. Memoization. Use a dictionary to memorize calls to edit_distance


def edit_distance(pattern, text, calls):
    # Lookup call
    key = pattern + ":" + text
    if key in calls:
        return calls[key]
    # Regular algorithm
    if len(pattern) == 0:
        return len(text)
    elif len(text) == 0:
        return len(pattern)
    else:
        if pattern[0] == text[0]:
            m_cost = edit_distance(pattern[1:], text[1:])
        else:
            m_cost = edit_distance(pattern[1:], text[1:]) + 1
        i_cost = edit_distance(pattern[:], text[1:]) + 1
        d_cost = edit_distance(pattern[1:], text[:]) + 1
        minimum = min(m_cost, i_cost, d_cost)
        # Store call
        calls[pattern + ":" + text] = minimum
        # Return
        return minimum


# 3. Dynamic Prgramming. Implement edit-distance computation using a dynamic programming table
def edit_distance_dp(pattern, text):
    # Init
    dp_matrix = [[0 for _ in range(len(text) + 1)] for _ in range(len(pattern) + 1)]
    for v in range(len(pattern) + 1):
        dp_matrix[v][0] = v
    for h in range(len(text) + 1):
        dp_matrix[0][h] = h
    # Compute DP Matrix
    for h in range(1, len(text) + 1):
        for v in range(1, len(pattern) + 1):
            dp_matrix[v][h] = min(
                dp_matrix[v - 1][h - 1] + (0 if pattern[v - 1] == text[h - 1] else 1),
                dp_matrix[v][h - 1] + 1,
                dp_matrix[v - 1][h] + 1)
    return dp_matrix


# 3. Dynamic Programming. Backtrace optimum CIGAR:


def backtrace_matrix(pattern, text, dp_matrix):
    v = len(pattern)
    h = len(text)
    cigar = []
    while v > 0 and h > 0:
        if dp_matrix[v][h] == dp_matrix[v - 1][h] + 1:
            v -= 1
            cigar.insert(0, "D")
        elif dp_matrix[v][h] == dp_matrix[v][h - 1] + 1:
            h -= 1
            cigar.insert(0, "I")
        else:
            v -= 1
            h -= 1
            if pattern[v] == text[h]:
                cigar.insert(0, "M")
            else:
                cigar.insert(0, "X")
    if v > 0:
        for _ in range(v): cigar.insert(0, "D")
    if h > 0:
        for _ in range(h): cigar.insert(0, "I")
    return cigar


# Compute edit distance
dp_matrix = edit_distance_dp("GATTACA", "GGACTCA")
# Print matrix
# [0, 1, 2, 3, 4, 5, 6, 7]
# [1, 0, 1, 2, 3, 4, 5, 6]
# [2, 1, 1, 1, 2, 3, 4, 5]
# [3, 2, 2, 2, 2, 2, 3, 4]
# [4, 3, 3, 3, 3, 2, 3, 4]
# [5, 4, 4, 3, 4, 3, 3, 3]
# [6, 5, 5, 4, 3, 4, 3, 4]
# [7, 6, 6, 5, 4, 4, 4, 3]
print_dp_matrix(dp_matrix)
# Prints "(2, ['I', 'M', 'M', 'M', 'M', 'D', 'M', 'M'])"
print(backtrace_matrix("GATTACA", "GGACTCA", dp_matrix))


# 4. Subset sum problem. Given a list of numbers, find out is a subset adds up to a given number
# Combinatorial exploration

def subset_sum(numbers, n, total):
    # Basic Cases
    if (total == 0): return True
    if (n == 0 and total != 0): return False
    # Last element is greater than sum
    if (numbers[n - 1] > total):
        return subset_sum(numbers, n - 1, total)
    # (1) Include the last element
    # (2) Exclude the last element
    return subset_sum(numbers, n - 1, total) or subset_sum(numbers, n - 1, total - numbers[n - 1])


numbers = [3, 14, 4, 12, 5, 3, 40]
total = 10
if (subset_sum(numbers, len(numbers), total)):
    print("Found a subset with given sum")
else:
    print("No subset with given sum")


# Dynamic
def subset_sum(numbers, n, total):
    subset = [[False for _ in range(total + 1)] for _ in range(n + 1)]
    # If sum is 0, then answer is true
    for i in range(n + 1):
        # Sum is 0
        subset[i][0] = True
        # Sum is not 0 and set is empty
        for i in range(1, total + 1):
            subset[0][i] = False
        # Fill the subset table (bottom up)
        for i in range(1, n + 1):
            for j in range(1, total + 1):
                if j < numbers[i - 1]:
                    subset[i][j] = subset[i - 1][j]
                if j >= numbers[i - 1]:
                    subset[i][j] = subset[i - 1][j] or subset[i - 1][j - numbers[i - 1]]
    return subset[n][total]


numbers = [3, 14, 4, 12, 5, 3, 40]
total = 10
if subset_sum(numbers, len(numbers), total):
    print("Found a subset with given sum")
else:
    print("No subset with given sum")
