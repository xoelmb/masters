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
    if len(numbers_list) != 1:
        left_list = numbers_list[:len(numbers_list) // 2]  # Left-half of the list
        right_list = numbers_list[len(numbers_list) // 2:]  # Right-half of the list
        # Sort recursively the halves
        merge_sort(left_list)
        merge_sort(right_list)
        # Merge both halves into the final sorted list
        merge_lists(left_list, right_list, numbers_list)


import random, time

numbers = []
for _ in range(0, 1000000):
    numbers.append(random.randint(1, 1000000))

t0 = time.time()
merge_sort(numbers)
print(time.time() - t0)
print(numbers)
