def get_par(args):
    parameters = {}
    last = ""
    for i in range(1, len(args)):
        if args[i][0:2:] == "--":
            parameters[args[i][2::]] = args[i + 1]
            last = args[i + 1]
        elif args[i] != last:
            print("Ignored argument:", args[i])
    return parameters


def check_par(parameters):
    print("Cal fer una funciò que comprobi que els parameters estan bé introduits.", parameters)





    return False


def get_format(input_file):
    fp = open(input_file, "r")
    for line in fp:
        if line[0] == ">":
            file_format = "FASTA"
        elif line[0] == "@":
            file_format = "FASTQ"
        else:
            file_format = False
        break
    fp.close()
    return file_format


def revcomp(input_file, output_file, file_format):
    comp_dic = {"A": "T", "C": "G", "G": "C", "T": "A", "N": "N", "a": "t", "c": "g", "g": "c", "t": "a", "n": "n"}
    new_file = open(output_file, "wt")
    with open(input_file, "r") as fp:
        while True:
            tag = fp.readline().rstrip()
            if not tag:
                break
            sequence = fp.readline().rstrip()
            try:
                revcomp = "".join(comp_dic[base] for base in sequence[::-1])
                new_file.write(tag + "\n" + revcomp + "\n")
                if file_format == "FASTQ":
                    fp.readline()
                    qual = fp.readline().rstrip()
                    revqual = "".join(qual[::-1])
                    new_file.write("+\n" + revqual + "\n")
            except:
                print(tag, "could not be processed.")
                if file_format == "FASTQ":
                    fp.readline()
                    fp.readline()


def trim(input_file, output_file, file_format, left, right):
    print("haha")
    return "okay"


def adaptor_removal(file, tag):
    print("hihi")
    return "okay"


test_arguments = ["name.py", "--input", "mbio.sample.fastq", "--output", "output_file.fastq", "--operation", "c",
                  "jeje"]

parameters = get_par(test_arguments)

# parameters.items()[-1]

if check_par(parameters) == False:
    print("Invalid arguments used. Exiting.")
    exit(1)

file_format = get_format(parameters["input"])
if file_format == False:
    print("Invalid file format. Exiting.")

if parameters["operation"] == "rc":
    revcomp(parameters["input"], parameters["output"], file_format)

elif parameters["operation"] == "trim":
    trim((parameters["input"], parameters["output"], file_format))
