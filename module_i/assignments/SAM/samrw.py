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


def compare_records(first, second):
    chr_order = {'chr1': 1, 'chr2': 2, 'chr3': 3, 'chr4': 4, 'chr5': 5, 'chr6': 6, 'chr7': 7, 'chr8': 8, 'chr9': 9,
                 'chr10': 10, 'chr11': 11, 'chr12': 12, 'chr13': 13, 'chr14': 14, 'chr15': 15, 'chr16': 16, 'chr17': 17,
                 'chr18': 18, 'chr19': 19, 'chr20': 20, 'chr21': 21, 'chr22': 22, 'chrX': 23, 'chrY': 24, '*': 25}

    if chr_order[first[2]] < chr_order[second[2]]:
        return True
    elif chr_order[first[2]] > chr_order[second[2]]:
        return False
    else:
        if first[3] <= second[3]:
            return True
        else:
            return False


def merge_sort(recordlist):
    # Checks if the length of the list is greater than 1
    if len(recordlist) > 1:
        # Compute middle point
        t = len(recordlist) // 2
        left_list = recordlist[:t]
        right_list = recordlist[t:]
        merge_sort(left_list)
        merge_sort(right_list)
        merge_lists(left_list, right_list, recordlist)
    return recordlist


def merge_lists(list1, list2, merged):
    p1 = 0
    p2 = 0
    pmerged = 0
    while p1 < len(list1) and p2 < len(list2):
        if compare_records(list1[p1], list2[p2]):
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

merge_sort(records)

with open('sorted_'+pars["input"], 'wt') as op:
    for header in headers:
        op.write(header)
    for record in records:
        op.write('\t'.join(record))
