########################################################################################################################
#################                                    ALGORITHMS 1                                    ###################
########################################################################################################################

# BLOCK EXERCISES

# [E0] Compute the complexity of the following algorithms. Taking into
# account that it has taken 50s to run for n=1000, calculate how long it
# will take to run for n=100000.


def sum_list(my_list):
    count = 0
    for elm in my_list:
        count += elm
    return count


# [E1] Compute the complexity of the following algorithms. Taking into
# account that it has taken 60s to run for n=140, calculate how long it
# will take to run for n=500.


def factorial(n):
    result = n
    for i in range(1, n):
        result *= i
    return result


# [E2] Compute the complexity of the following algorithms. Taking into
# account that it has taken 40s to run for n=10, calculate how long it
# will take to run for n=1000.


def remove_adaptor_list(sequence, adaptor_list):
    for adaptor in adaptor_list:
        if sequence[0:len(adaptor)] == adaptor:
            return sequence[len(adaptor):]
    return sequence


# [E3] Compute the complexity of the following algorithms. Taking into
# account that it has taken 90s to run for n=100, calculate how long it
# will take to run for n=200.


def reverse(sequence):
    sequence_rev = ""
    for i in range(1, len(sequence) + 1):
        sequence_rev += sequence[len(sequence) - i]
    return sequence_rev


# [E4] Compute the complexity of the following algorithms. Taking into
# account that it has taken 30s to run for n=10, calculate how long it
# will take to run for n=100.


def reverse_complement(dna):
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    return ''.join([complement[base] for base in dna[::-1]])


# [E5] Compute the complexity of the following algorithms. Taking into
# account that it has taken 33s to run for n=100, calculate how long it
# will take to run for n=1000.


def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n - 1)


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


# Searching a number in a list. Recursively.


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

# Kmers
kmers = ["CGT","TAG","AAA"]
# Sort kmers
sort_kmers(kmers)
# Prints "["AAA","CGT","TAG"]"
print(kmers)


# [E3] Given 3 sorted lists of kmers, implement a function that
# produces the merged sorted list of the three.


# [E2] Implement a function that binary searches a kmer within a
# sorted list of kmers


# [E4] Given a list of sorted lists of kmers, implement a function that
# produces the resulting merged sorted list of all.


# [E5] Given a sorted list of integers, implement a ternary search that,
# in the spirit of the binary search, divides the search space by 3 on
# each step of the search
