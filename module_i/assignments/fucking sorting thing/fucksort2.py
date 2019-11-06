def merge_sort(l):
    # Checking that the length of the (split) list is grater than 1
    if len(l) > 1:
        # Calculate the middle point
        t = len(l) // 2
        # Dividing the list of numbers, recursively pass it to merge_sort and making it iterable
        # Instead of using pointers, iterate using iter/next
        it1 = iter(merge_sort(l[:t]))
        x1 = next(it1)
        it2 = iter(merge_sort(l[t:]))
        x2 = next(it2)
        # Define the ordered list as an empty list
        l = []
        # Try will expand the list and iterate using next. When one of the list has been finished, it raises an error
        # so the except is called.
        try:
            while True:
                if x1 <= x2:
                    l.append(x1)
                    x1 = next(it1)
                else:
                    l.append(x2)
                    x2 = next(it2)
        # Except checks which of the list has been completed, and appends the other one with append/extend.
        except:
            if x1 <= x2:
                l.append(x2)
                l.extend(it2)
            else:
                l.append(x1)
                l.extend(it1)
    return l


import random, time

numbers = []
for _ in range(0, 1000000):
    numbers.append(random.randint(1, 1000000))

t0 = time.time()
merge_sort(numbers)
print(time.time() - t0)
