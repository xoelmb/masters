# Implement a python script that, given a SAM file and two chromosome coordinates (i.e. chromosome:position),
# prints all the sequences in the SAM file that overlap the specified range.
# • The python script must implement a O(log(n)) merge sort algorithm to sort all SAM records read from the input file.
# • Then, it has to perform a search to locate all SAM records overlapping the coordinates specified between the
# “--from” and “--to” parameters. All searches have to be binary searches.


import sys
import re


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


def compare_records(first, second, pos_field=3):
    chr_order = {'chr1': 1, 'chr2': 2, 'chr3': 3, 'chr4': 4, 'chr5': 5, 'chr6': 6, 'chr7': 7, 'chr8': 8, 'chr9': 9,
                 'chr10': 10, 'chr11': 11, 'chr12': 12, 'chr13': 13, 'chr14': 14, 'chr15': 15, 'chr16': 16, 'chr17': 17,
                 'chr18': 18, 'chr19': 19, 'chr20': 20, 'chr21': 21, 'chr22': 22, 'chrX': 23, 'chrY': 24, '*': 25}

    if chr_order[first[2]] < chr_order[second[2]]:
        return 1
    elif chr_order[first[2]] > chr_order[second[2]]:
        return 2
    else:
        if first[pos_field] == '*':
            return 2
        elif second[pos_field] == '*':
            return 1
        elif first[pos_field] == '*' and second[pos_field] == '*':
            return 0
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
        # Compute middle point
        t = len(recordlist) // 2
        left_list = recordlist[:t]
        right_list = recordlist[t:]
        merge_sort(left_list)
        merge_sort(right_list)
        merge_lists(left_list, right_list, recordlist, pos_field)
    return recordlist


def merge_lists(list1, list2, merged, pos_field=3):
    p1 = 0
    p2 = 0
    pmerged = 0
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


def bin_search(rec_list, item, pos_field=3):
    if len(rec_list) > 1:
        middle = len(rec_list) // 2
        comparison = compare_records(rec_list[middle], item, pos_field)
        if comparison == 0:
            return middle
        elif comparison == 1:
            return middle + bin_search(rec_list[middle::], item, pos_field)
        else:
            return bin_search(rec_list[:middle:], item, pos_field)
    elif len(rec_list) == 1:
        if compare_records(rec_list[0], item, pos_field) == 1:
            return 1
        else:
            return 0
    else:
        return 0


def compute_end(rec_list):
    for record in rec_list:
        if record[3].isdigit():
            length = 0
            cigar = record[5]
            matches = re.compile(r'(\d+)[MDN=X]')
            for match in matches.finditer(cigar):
                length += int(match.group(1))
            record.append(str(length+int(record[3])))
        else:
            record.append('*')


# Parse arguments.
if len(sys.argv) != 6:
    print("Provide valid arguments")
    exit(1)
pars = {"input": sys.argv[1], "from": ['', ''], "to": ['', '']}
for i in range(2, len(sys.argv)):
    if sys.argv[i] == "--from":
        pars["from"].extend(sys.argv[i + 1].split(':'))
    elif sys.argv[i] == "--to":
        pars["to"].extend(sys.argv[i + 1].split(':'))

# Open sam file, store headers in a list, and records in another list.
headers, records = open_sam(pars["input"])

merge_sort(records)

with open('sorted_' + pars["input"], 'wt') as op:
    for header in headers:
        op.write(header)
    for record in records:
        op.write('\t'.join(record))

start_idx = bin_search(records, pars['from'])
end_idx = bin_search(records, pars['to'])
found_records = records[start_idx:end_idx]
records = records[:start_idx]
compute_end(records)
merge_sort(records, pos_field=-1)
left_idx = bin_search(records, pars['from'], pos_field=-1)
for rec in records[left_idx:]:
    found_records.append(rec[:-1])

with open('found_' + pars["input"], 'wt') as op:
    for header in headers:
        op.write(header)
    for record in found_records:
        op.write('\t'.join(record))
