import sys, re


class Read:
    def __init__(self, seq=None, qual=None):
        self.sequence = seq
        self.quality = qual


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
            if base in self.bases_dic.keys():
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
            if base in self.trim_dic.keys():
                self.trim_dic[base] += 1
            self.trim_total += 1

    def add_adaptor(self):
        self.adaptors += 1

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


def revcomp(unprocessed_read, content):
    comp_dic = {"A": "T", "C": "G", "G": "C", "T": "A", "N": "N", "a": "t", "c": "g", "g": "c", "t": "a", "n": "n"}
    processed_read = Read()
    try:
        processed_read.sequence = "".join(comp_dic[base] for base in unprocessed_read.sequence[::-1])
        if unprocessed_read.quality:
            processed_read.quality = "".join(unprocessed_read.quality[::-1])
        content.add_seq(unprocessed_read.sequence)
        return processed_read
    except:
        return None


def trim(unprocessed_read, left, right, content):
    processed_read = Read()
    try:
        processed_read.sequence = unprocessed_read.sequence[left:right:]
        if unprocessed_read.quality:
            processed_read.quality = unprocessed_read.quality[left:right:]
        content.add_seq(unprocessed_read.sequence)
        content.add_trim(unprocessed_read.sequence, left, right)
        return processed_read
    except:
        return None


def adaptor_removal(unprocessed_read, adaptor, content):
    processed_read = Read()
    try:
        if unprocessed_read.sequence[:len(adaptor):].upper() == adaptor.upper():
            processed_read.sequence = unprocessed_read.sequence[len(adaptor)::]
            if unprocessed_read.quality:
                processed_read.quality = unprocessed_read.quality[len(adaptor)::]
            content.add_adaptor()
        else:
            processed_read.sequence = unprocessed_read.sequence
            processed_read.quality = unprocessed_read.quality
        content.add_seq(unprocessed_read.sequence)
        return processed_read
    except:
        return None


# test_arguments = ["name.py", "--input", "mbio.sample.fastq", "--output", "output_file.fastq", "--operation", "adaptor_removal", "--adaptor", "AGT"]
parameters = get_par(sys.argv)

if check_par(parameters) is False:
    print("Invalid arguments used. Exiting.")
    exit(1)

if parameters["operation"] == "trim":
    if not "trim-left" in parameters.keys():
        parameters["trim-left"] = 0
    else:
        parameters["trim-left"] = int(parameters["trim-left"])
    if not "trim-right" in parameters.keys():
        parameters["trim-right"] = None
    else:
        parameters["trim-right"] = int(parameters["trim-right"]) * -1

parameters["format"] = get_format(parameters["input"])

if parameters["format"] is False:
    print("Invalid file format. Exiting.")
    exit(1)

new_file = open(parameters["output"], "wt")
content = Summary()

with open(parameters["input"], "rt") as fp:
    while True:
        tag = fp.readline().rstrip()
        if not tag:
            break
        sequence = fp.readline().rstrip()
        current_read = Read(sequence)
        if parameters["format"] == "FASTQ":
            fp.readline()
            quality = fp.readline().rstrip()
            current_read.quality = quality

        if parameters["operation"] == "rc":
            processed_read = revcomp(current_read, content)
        elif parameters["operation"] == "trim":
            processed_read = trim(current_read, parameters["trim-left"], parameters["trim-right"], content)
        else:
            processed_read = adaptor_removal(current_read, parameters["adaptor"], content)

        if processed_read:
            new_file.write(tag + "\n" + processed_read.sequence + "\n")
            if processed_read.quality:
                new_file.write("+\n" + processed_read.quality + "\n")
        else:
            print(tag, "could not be processed.")

new_file.close()

content.report(parameters["operation"])

print("\nFile processed successfully.")
exit(0)
