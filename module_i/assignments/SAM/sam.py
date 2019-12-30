# Implement a python script that, given a SAM file and two chromosome coordinates (i.e. chromosome:position),
# prints all the sequences in the SAM file that overlap the specified range.
# • The python script must implement a O(log(n)) merge sort algorithm to sort all SAM records read from the input file.
# • Then, it has to perform a search to locate all SAM records overlapping the coordinates specified between the
# “--from” and “--to” parameters. All searches have to be binary searches.


import sys


# Opens the sam file and returns headers as a list, and records as a nested list.
def open_sam(filename):
    heads = []
    recs = []
    with open(filename, "rt") as f:
        while True:
            line = f.readline()
            if not line:
                break
            if line[0] == "@":
                heads.append(line)
            else:
                recs.append(line.split("\t"))
    return heads, recs


def comparerecords(first, second):
    if first[2] < second[2]:
        return True
    elif first[2] > second[2]:
        return False
    else:
        if first[3] <= second[3]:
            return True
        else:
            return False


def mergesort_sam(recordlist):
    # Checks if the length of the list is greater than 1
    if len(recordlist) > 1:
        # Compute middle point
        t = len(recordlist) // 2
        # Dividing the list of numbers, recursively pass it to merge_sort and making it iterable
        # Instead of using pointers, iterate using iter/next
        left_list = iter(mergesort_sam(recordlist[:t]))
        n1 = next(left_list)
        right_list = iter(mergesort_sam(recordlist[t:]))
        n2 = next(right_list)
        # Define the ordered list as an empty list
        recordlist = []
        # Try will expand the list and iterate using next. When one of the list has been finished, it raises an error
        # so the except is called.
        try:
            while True:
                if comparerecords(n1, n2):
                    recordlist.append(n1)
                    n1 = next(left_list)
                else:
                    recordlist.append(n2)
                    n2 = next(right_list)
        # Except checks which of the list has been completed, and appends the other one with append/extend.
        except:
            if n1 <= n2:
                recordlist.append(n2)
                recordlist.extend(right_list)
            else:
                recordlist.append(n1)
                recordlist.extend(left_list)
    return recordlist


# Parse arguments.
if len(sys.argv) != 6:
    print("Provide valid arguments")
    exit(1)
pars = {"input": sys.argv[1]}
for i in range(2, len(sys.argv)):
    if sys.argv[i] == "--from":
        pars["from"] = sys.argv[i + 1]
    elif sys.argv[i] == "--to":
        pars["to"] = sys.argv[i + 1]

# Open sam file, store headers in a list, and records in another list.
headers, records = open_sam(pars["input"])

sortedrecords = mergesort_sam(records)

with open('oredertest.sam', 'wt') as op:
    for record in sortedrecords:
        op.write('\t'.join(record))
