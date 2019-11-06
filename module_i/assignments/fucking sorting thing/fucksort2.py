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


import random, time

numbers = [random.randint(1, 1000000) for _ in range(0,1000000)]

t0 = time.time()
merge_sort(numbers)
print(time.time() - t0)
