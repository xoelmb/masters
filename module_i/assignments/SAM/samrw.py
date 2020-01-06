# Implement a python script that, given a SAM file and two chromosome coordinates (i.e. chromosome:position),
# prints all the sequences in the SAM file that overlap the specified range.
# • The python script must implement a O(log(n)) merge sort algorithm to sort all SAM records read from the input file.
# • Then, it has to perform a search to locate all SAM records overlapping the coordinates specified between the
# “--from” and “--to” parameters. All searches have to be binary searches.


import sys
import re


# Opens the sam file and returns all mapped records as a nested list. Unmapped records can not match the input interval.
def open_sam(filename):
    recs = []
    with open(filename, "rt") as f:
        while True:
            line = f.readline()
            if not line:
                break
            if line[0] != "@":
                rec = line.split("\t")
                if rec[2] != '*' and rec[3] != '*':
                    recs.append(rec)
    return recs


# Compares two records in a SAM format. Allows to select the field to sort all the entries.
def compare_records(first, second, pos_field=3):
    try:
        chr_order
    except NameError:
        chr_order = {'chr1': 1, 'chr2': 2, 'chr3': 3, 'chr4': 4, 'chr5': 5, 'chr6': 6, 'chr7': 7, 'chr8': 8, 'chr9': 9,
                     'chr10': 10, 'chr11': 11, 'chr12': 12, 'chr13': 13, 'chr14': 14, 'chr15': 15, 'chr16': 16,
                     'chr17': 17, 'chr18': 18, 'chr19': 19, 'chr20': 20, 'chr21': 21, 'chr22': 22, 'chrX': 23,
                     'chrY': 24}

    if chr_order[first[2]] < chr_order[second[2]]:
        return 1
    elif chr_order[first[2]] > chr_order[second[2]]:
        return 2
    else:
        if int(first[pos_field]) < int(second[pos_field]):
            return 1
        elif int(first[pos_field]) > int(second[pos_field]):
            return 2
        else:
            return 0


def merge_sort(recordlist, pos_field=3):
    # Checks if the length of the list is greater than 1
    if len(recordlist) > 1:
        # Computes middle point and recursively divide the list casting the resulting lists to the same function.
        t = len(recordlist) // 2
        left_list = recordlist[:t]
        right_list = recordlist[t:]
        merge_sort(left_list)
        merge_sort(right_list)
        # Merges sorted lists into another sorted list.
        merge_lists(left_list, right_list, recordlist, pos_field)
    return recordlist


# Merges sorted lists into another sorted list.
def merge_lists(list1, list2, merged, pos_field=3):
    # Initializing pointers for each of the working lists.
    p1 = 0
    p2 = 0
    pmerged = 0
    # Traverses the lists and selects the record that needs to go first in the final list.
    while p1 < len(list1) and p2 < len(list2):
        if compare_records(list1[p1], list2[p2], pos_field) < 2:
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


# Searches for the index of the first element from a sorted list of SAM records that is greater than a given value.
# Allows to specify the field to use for sorting (used to solve one limitation of this approach).
def bin_search(rec_list, item, pos_field=3):
    # Given a list of several elements, compares the element in the middle to a given element.
    if len(rec_list) > 1:
        middle = len(rec_list) // 2
        comparison = compare_records(rec_list[middle], item, pos_field)
        # Depending on the comparison, returns the index and/or continues the search in one of the halves of the list.
        if comparison == 0:
            return middle
        elif comparison == 1:
            return middle + bin_search(rec_list[middle::], item, pos_field)
        else:
            return bin_search(rec_list[:middle:], item, pos_field)
    # If there's only element left, compares it to the given record and adds 1 to the index accordingly.
    elif len(rec_list) == 1:
        if compare_records(rec_list[0], item, pos_field) == 1:
            return 1
        else:
            return 0
    # If the division of the list produces an empty list, it does not modify the final index.
    else:
        return 0


# This function computes the length of the alignment from its CIGAR string. Then computes the ending position and
# appends it to the record.
def compute_end(rec_list):
    for rec in rec_list:
        length = 0
        cigar = rec[5]
        # Which letters need to be added to compute the final position of the alignment was inferred from the SAM docs.
        matches = re.compile(r'(\d+)[MDN=X]')
        for match in matches.finditer(cigar):
            length += int(match.group(1))
        rec.append(str(length + int(rec[3])))


# Parses the arguments without checking them exhaustively.
if len(sys.argv) != 6:
    print("Provide valid arguments")
    exit(1)

# Stores the parameters in a dictionary. From and to values are formatted to somehow match the SAM format.
pars = {"input": sys.argv[1], "from": ['', ''], "to": ['', '']}
for i in range(2, len(sys.argv)):
    if sys.argv[i] == "--from":
        pars["from"].extend(sys.argv[i + 1].split(':'))
    elif sys.argv[i] == "--to":
        pars["to"].extend(sys.argv[i + 1].split(':'))

# Opens the sam file and stores the records in a nested list.
records = open_sam(pars["input"])

# Sorts the records.
merge_sort(records)

# Find the indexes of the first and final record whose starting position belongs to the interval.
start_idx = bin_search(records, pars['from'])
end_idx = bin_search(records, pars['to'])

# Stores those records in another list. We'll only keep the records previous to the previously found.
found_records = records[start_idx:end_idx]
records = records[:start_idx]

# Even if the starting position of an alignment does not belong to the interval, an alignment can overlap the interval
# if its final position belongs to the interval. To solve that, we compute the final position of the previous records.
compute_end(records)

# Then, we sort them according to the final position of the alignment.
merge_sort(records, pos_field=-1)

# This finds the first of the newly sorted records that belong to the interval, and appends them to the found list but
# removing the computed final positions.
left_idx = bin_search(records, pars['from'], pos_field=-1)
for rec in records[left_idx:]:
    found_records.append(rec[:-1])

# Optionally, resorts the found list by their starting positions.
merge_sort(found_records)

# Prints the records.
for record in found_records:
    print('\t'.join(record), end="")
