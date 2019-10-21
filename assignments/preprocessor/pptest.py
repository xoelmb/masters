import sys, re


class Summary:
    def __init__(self):
        self.bases_dic = {"A": 0, "C": 0, "G": 0, "T": 0, "N": 0}
        self.bases_total = 0
        self.seqs = 0
        self.adaptors = 0
        self.trim_dic = {"A": 0, "C": 0, "G": 0, "T": 0, "N": 0}
        self.trim_total = 0

    def add_seq(self, sequence):
        self.seqs += 1
        for base in sequence[::].upper():
            self.bases_dic[base] += 1
            self.bases_total += 1

    def add_trim(self, sequence, left, right):
        seq_left = ""
        seq_right = ""
        if left != 0:
            seq_left = sequence[:left:]
        if right is not None:
            seq_right = sequence[right::]
        removed = seq_left + seq_right
        for base in removed[::].upper():
            self.trim_dic[base] += 1
            self.trim_total += 1

    def report(self, mode):
        print("\n\nSummary:")
        print("\t" + str(self.seqs), "reads processed")
        print("\t" + str(self.bases_total), "bases processed (", end="")
        for base in ["A", "C", "G", "T", "N"]:
            print(str(int(self.bases_dic[base] / self.bases_total * 100)) + "%", base, end="")
            if base != "N":
                print(", ", end="")
            else:
                print(")")

        if mode == "trim":
            print("\t" + str(self.trim_total), "bases trimmed (", end="")
            for base in ["A", "C", "G", "T", "N"]:
                print(str(int(self.trim_dic[base] / self.trim_total * 100)) + "%", base, end="")
                if base != "N":
                    print(", ", end="")
                else:
                    print(")")

        elif mode == "adaptor_removal":
            print("\t" + str(self.adaptors) + " adaptors found")


def get_par(args):
    parameters = {}
    last = ""
    for i in range(1, len(args)):
        if args[i][0:2:] == "--" and i != len(args) - 1:
            parameters[args[i][2::]] = args[i + 1]
            last = args[i + 1]
        elif args[i] != last:
            print("Ignored argument:", args[i])
    return parameters


def check_par(parameters):
    tag_input, tag_output, tag_operation, tag_left, tag_right, tag_adaptor = False, False, False, False, False, False
    for k, v in parameters.items():
        if k == "input":
            try:
                f = open(v, "rt")
                f.close()
                tag_input = True
            except:
                print("Input file was not found.")
        elif k == "output":
            tag_output = True
        elif k == "operation":
            if v in ["rc", "trim", "adaptor_removal"]:
                tag_operation = True
            else:
                print("Invalid operation:", v + ".\n\trc, trim or adaptor_removal is expected.")
        elif k == "trim-left":
            try:
                if int(v) > 0:
                    tag_left = True
                else:
                    raise ()
            except:
                print("Invalid trim-left value. A >0 value is expected.")
        elif k == "trim-right":
            try:
                if int(v) > 0:
                    tag_right = True
                else:
                    raise ()
            except:
                print("Invalid trim-right value. A >0 value is expected.")
        elif k == "adaptor":
            if re.search(r'\A[ACGTNacgtn]*\Z', v):
                tag_adaptor = True
            else:
                print("Adaptor sequence is not valid. Only [ACGTNacgtn] bases are allowed.")
        else:
            print("Ignored argument:", k, v)
    if (tag_input, tag_output, tag_operation) == (True, True, True):
        if parameters["operation"] == "adaptor" and tag_adaptor is True:
            return True
        elif parameters["operation"] == "trim" and (tag_left is True or tag_right is True):
            return True
        else:
            return True
    else:
        return False


def get_format(input_file):
    fp = open(input_file, "r")
    file_format = False
    for line in fp:
        if line[0] == ">":
            file_format = "FASTA"
        elif line[0] == "@":
            file_format = "FASTQ"
        break
    fp.close()
    return file_format


def revcomp(input_file, output_file, file_format):
    comp_dic = {"A": "T", "C": "G", "G": "C", "T": "A", "N": "N", "a": "t", "c": "g", "g": "c", "t": "a",
                "n": "n"}
    new_file = open(output_file, "wt")
    content = Summary()
    with open(input_file, "r") as fp:
        while True:
            tag = fp.readline().rstrip()
            if not tag:
                break
            sequence = fp.readline().rstrip()
            print("It's a new seq.")
            try:
                revcomp = "".join(comp_dic[base] for base in sequence[::-1])
                new_file.write(tag + "\n" + revcomp + "\n")
                content.add_seq(sequence)
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
    content.report("rc")
    new_file.close()


def trim(input_file, output_file, file_format, left, right):
    new_file = open(output_file, "wt")
    content = Summary()
    with open(input_file, "r") as fp:
        while True:
            tag = fp.readline().rstrip()
            if not tag:
                break
            sequence = fp.readline().rstrip()
            print("It's a new seq.")
            try:
                trimseq = sequence[left:right:]
                new_file.write(tag + "\n" + trimseq + "\n")
                content.add_seq(sequence)
                content.add_trim(sequence, left, right)
                if file_format == "FASTQ":
                    fp.readline()
                    qual = fp.readline().rstrip()
                    trimqual = qual[left:-right:]
                    new_file.write("+\n" + trimqual + "\n")
            except:
                print(tag, "could not be processed.")
                if file_format == "FASTQ":
                    fp.readline()
                    fp.readline()
    new_file.close()
    content.report("trim")


def adaptor_removal(input_file, output_file, file_format, adaptor):
    adaptor_up = adaptor.upper()
    new_file = open(output_file, "wt")
    content = Summary()
    with open(input_file, "r") as fp:
        while True:
            tag = fp.readline().rstrip()
            if not tag:
                break
            sequence = fp.readline().rstrip()
            print("It's a new seq.")
            try:
                seq_up = sequence[:len(adaptor_up):].upper()
                match = True
                for i in range(len(adaptor_up)):
                    if adaptor_up[i] != "N" and seq_up[i] != "N" and adaptor_up[i] != seq_up[i]:
                        match = False
                        break
                if match is True:
                    new_seq = sequence[len(adaptor)::]
                    new_file.write(tag + "\n" + new_seq + "\n")
                    content.adaptors += 1
                    if file_format == "FASTQ":
                        fp.readline()
                        qual = fp.readline().rstrip()
                        new_qual = qual[len(adaptor)::]
                        new_file.write("+\n" + new_qual + "\n")
                else:
                    new_file.write(tag + "\n" + sequence + "\n")
                    if file_format == "FASTQ":
                        fp.readline()
                        qual = fp.readline().rstrip()
                        new_file.write("+\n" + qual + "\n")
                content.add_seq(sequence)
            except:
                print(tag, "could not be processed.")
                if file_format == "FASTQ":
                    fp.readline()
                    fp.readline()
    new_file.close()
    content.report("adaptor_removal")


test_arguments = ["name.py", "--input", "mbio.sample.fastq", "--output", "output_file.fastq", "--operation",
                  "adaptor_removal", "jeje", "--probe", "wrong", "--adaptor", "GGGTTT", "--trim-left", "10",
                  "--trim-right", "6"]

parameters = get_par(test_arguments)

if check_par(parameters) is False:
    print("Invalid arguments used. Exiting.")
    exit(1)

parameters["format"] = get_format(parameters["input"])

if parameters["format"] is False:
    print("Invalid file format. Exiting.")
    exit(1)

if parameters["operation"] == "rc":
    revcomp(parameters["input"], parameters["output"], parameters["format"])

elif parameters["operation"] == "trim":
    if not "trim-left" in parameters.keys():
        parameters["trim-left"] = 0
    else:
        parameters["trim-left"] = int(parameters["trim-left"])

    if not "trim-right" in parameters.keys():
        parameters["trim-right"] = None
    else:
        parameters["trim-right"] = int(parameters["trim-right"]) * -1

    trim(parameters["input"], parameters["output"], parameters["format"], parameters["trim-left"],
         parameters["trim-right"])

else:
    adaptor_removal(parameters["input"], parameters["output"], parameters["format"], parameters["adaptor"])

print("\nFile processed successfully.")
exit(0)
