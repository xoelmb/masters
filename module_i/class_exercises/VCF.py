def compare_vcf(vcf1, vcf2):
    chrlist = ["Chr1", "Chr2", "Chr3", "Chr4", "Chr5", "Chr6", "Chr7", "Chr8", "Chr9", "Chr10", "Chr11", "Chr12",
               "Chr13", "Chr14", "Chr15", "Chr16", "Chr17", "Chr18", "Chr19", "Chr20", "Chr21", "Chr22", "ChrX", "ChrY"]

    if chrlist.index(vcf1[0]) < chrlist.index(vcf2[0]):
        return -1
    elif chrlist.index(vcf1[0]) > chrlist.index(vcf2[0]):
        return +1
    else:
        if vcf1[1] < vcf2[1]:
            return -1
        elif vcf1[1] > vcf2[1]:
            return +1
        else:
            return 0


def sort_2vcf(vcf1, vcf2):
    if compare_vcf(vcf1, vcf2) <= 0:
        return [vcf1, vcf2]

    else:
        return [vcf2, vcf1]


def merge_vcf_lists(list1,list2,merged):
    p1 = 0
    p2 = 0
    pmerged = 0
    # Merge both list by comparing each element at the head
    while p1 < len(list1) and p2 < len(list2):
        if compare_vcf(list1[p1],list2[p2]) <= 0:
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


# Prints "0"
print(compare_vcf(("Chr1", 45798901, "GTGTGT", ""), ("Chr1", 45798901, "C", "T")))
# Prints "-1"
print(compare_vcf(("Chr1", 45798901, "C", "T"), ("Chr2", 793301, "GTGTGT", "")))
# Prints "1"
print(compare_vcf(("Chr2", 793301, "GTGTGT", ""), ("Chr1", 45798901, "C", "T")))


# Sample data
list1 = [("Chr1",100,"C","T"),("Chr3",20,"C","T")]
list2 = [("Chr1",900,"C","T")]
merged = [0] * (len(list1) + len(list2)) # Declare empty list
# Merge list of VCF records
merge_vcf_lists(list1,list2,merged)
# Prints "[('Chr1', 100, 'C', 'T'), ('Chr1', 900, 'C', 'T'), ('Chr3', 20, 'C', 'T')]"
print(merged)


def merge(list1, list2, nmerged):
    p1 = 0
    p2 = 0
    pmerged = 0
    # Merge both list by comparing each element at the head
    while p1 < len(list1) and p2 < len(list2):
        if list1[p1] <= list2[p2]:
            nmerged[pmerged] = list1[p1]
            p1 += 1
        else:
            nmerged[pmerged] = list2[p2]
            p2 += 1
        pmerged += 1
    # Append the remaining elements of list1
    while p1 < len(list1):
        nmerged[pmerged] = list1[p1]
        p1 += 1
        pmerged += 1
    # Append the remaining elements of list2
    while p2 < len(list2):
        nmerged[pmerged] = list2[p2]
        p2 += 1
        pmerged += 1


def merge_sort(numbers_list):
    if len(numbers_list) == 1:
        return
    else:
        middle_point = len(numbers_list)//2
        left = numbers_list[:middle_point]
        right = numbers_list[middle_point:]

        merge_sort(left)
        merge_sort(right)

        merge(left,right, nmerged)


numbersss = [1,5,3,96,98,7,5,6,1,854,65,46,5841,6874]
nmerged = [0] * len(numbersss)
merge_sort(numbersss)
print(nmerged)

