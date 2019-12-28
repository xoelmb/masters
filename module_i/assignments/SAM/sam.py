# Implement a python script that, given a SAM file and two chromosome coordinates (i.e. chromosome:position),
# prints all the sequences in the SAM file that overlap the specified range.
# • The python script must implement a O(log(n)) merge sort algorithm to sort all SAM records read from the input file.
# • Then, it has to perform a search to locate all SAM records overlapping the coordinates specified between the
# “--from” and “--to” parameters. All searches have to be binary searches.


def open_sam(input_file):
    heads = []
    recs = []
    with open(input_file, "rt") as f:
        while True:
            line = f.readline()
            if not line:
                break
            if line[0] == "@":
                heads.append(line)
            else:
                recs.append(line.split("\t"))
    return heads, recs

# Parse arguments.
import sys
pars = {"input": sys.argv[1]}
for i in range(2, len(sys.argv)):
    if sys.argv[i] == "--from":
        try:
            pars["from"] = int(sys.argv[i+1])
        except:
            print("Provide a valid --from value")
            exit(1)
    elif sys.argv[i] == "--to":
        try:
            pars["to"] == sys.argv[i+1]
        except:
            print("Provide a valid --to value")
            exit(1)

# Open sam file, store headers in a list, and records in another list.


