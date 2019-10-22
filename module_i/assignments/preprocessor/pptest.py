import re
import sys


class Read:  # Class used to store sequence and quality of a given read
    def __init__(self, seq=None, qual=None):
        self.sequence = seq
        self.quality = qual


class Summary:  # Class used to store different data of the whole operation
    def __init__(self):
        self.bases_dic = {"A": 0, "C": 0, "G": 0, "T": 0, "N": 0}
        self.bases_total = 0
        self.seqs = 0
        self.adaptors = 0
        self.trim_dic = {"A": 0, "C": 0, "G": 0, "T": 0, "N": 0}
        self.trim_total = 0

    def add_seq(self, sequence):  # Function to update statistics on the analysis when a sequence is processed
        self.seqs += 1
        for base in sequence[::].upper():
            if base in self.bases_dic.keys():
                self.bases_dic[base] += 1
            self.bases_total += 1

    def add_trim(self, sequence, left, right):  # Update statistics when a trim operation is performed
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

    def add_adaptor(self):  # Update statistics when a adaptor is found
        self.adaptors += 1

    def report(self, mode):  # Function to print statistics depending on the operation performed
        print("\n\nSummary:\n\t" + str(self.seqs), "reads processed\n\t" + str(self.bases_total), "bases processed (",
              end="")
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


def get_par(args):  # Function to parse the arguments used by the user
    parameters = {}  # Dictionary used to store the parameters
    last = ""  # Initialize a variable that stores the last value added to the dictionary
    for i in range(1, len(args)):  # Iterate over arguments, except for the first one (name of file)
        if args[i][0:2:] == "--" and i != len(args) - 1:  # Checks if the argument is a parameter and not the last one
            parameters[args[i][2::]] = args[i + 1]  # Stores the next argument as the value of a given parameter
            last = args[i + 1]  # Updates the last value stored
        elif args[i] != last:  # If an argument has not been preceded by a "--parameter", it's ignored
            print("Ignored argument:", args[i])
    return parameters  # Returns the whole dictionary of parameters


def check_par(parameters):  # Function that checks the validity of the parsed arguments. Returns True or False.
    # The tags are used to check if a parameter has been properly added
    tag_input, tag_output, tag_operation, tag_left, tag_right, tag_adaptor = False, False, False, False, False, False
    for k, v in parameters.items():  # Iterate over the parameters
        if k == "input":
            try:  # Checks if input file can be opened
                f = open(v, "rt")
                f.close()
                tag_input = True
            except:
                print("Input file was not found.")
        elif k == "output":  # Checks if an output file name has been provided
            tag_output = True
        elif k == "operation":  # Checks if an operation parameter has been provided and if it's valid
            if v in ["rc", "trim", "adaptor_removal"]:
                tag_operation = True
            else:
                print("Invalid operation:", v + ".\n\trc, trim or adaptor_removal is expected.")
        elif k == "trim-left":  # Checks if the left-trim parameter is a valid number
            try:
                if int(v) > 0:
                    tag_left = True
                else:
                    raise ()
            except:
                print("Invalid trim-left value. A >0 value is expected.")
        elif k == "trim-right":  # Checks if the right-trim parameter is a valid number
            try:
                if int(v) > 0:
                    tag_right = True
                else:
                    raise ()
            except:
                print("Invalid trim-right value. A >0 value is expected.")
        elif k == "adaptor":  # Checks if the adaptor string is valid.
            if re.search(r'\A[ACGTNacgtn]*\Z', v):
                tag_adaptor = True
            else:
                print("The provided adaptor sequence is not valid. Only [ACGTNacgtn] bases are allowed.")
        else:  # If any other argument is provided, it will be ignored.
            print("Ignored argument:", k, v)
    if (tag_input, tag_output, tag_operation) == (True, True, True):  # Checks if the minimum parameters are provided
        if parameters["operation"] == "adaptor_removal":  # If adaptor_removal, checks if there's a valid adaptor
            if tag_adaptor is True:
                return True
            else:
                print("A valid adaptor sequence is needed.")
        elif parameters["operation"] == "trim":  # If trim, checks if there are any valid trimming parameter
            if tag_left is True or tag_right is True:
                return True
            else:
                print("A valid trimming value is needed.")
        elif parameters["operation"] == "rc":
            return True
    return False  # Returns False if the previous checks are not fulfilled


def get_format(input_file):  # Function to get the format of the input file
    file = open(input_file, "r")
    file_format = False
    line = file.readline()
    if line[0] == ">":
        file_format = "FASTA"
    elif line[0] == "@":
        file_format = "FASTQ"
    file.close()
    return file_format


def revcomp(unprocessed, content):  # Performs reverse-complement on a given sequence and quality if needed
    comp_dic = {"A": "T", "C": "G", "G": "C", "T": "A", "N": "N", "a": "t", "c": "g", "g": "c", "t": "a", "n": "n"}
    processed = Read()  # Initializes the resulting read
    try:
        processed.sequence = "".join(comp_dic[base] for base in unprocessed.sequence[::-1])  # Revcom the sequence
        if unprocessed.quality:  # Reverses the qualities if the read contains any
            processed.quality = "".join(unprocessed.quality[::-1])
        content.add_seq(unprocessed.sequence)  # Updates the statistics
        return processed  # Returns a processed read
    except:  # If the read cannot be processed, a None is returned
        return None


def trim(unprocessed, left, right, content):  # Performs trimming on a given sequence and quality if needed
    processed = Read()  # Initializes the resulting read
    try:
        processed.sequence = unprocessed.sequence[left:right:]  # Trims the sequence
        if unprocessed.quality:  # Trims the qualities if the read contains any
            processed.quality = unprocessed.quality[left:right:]
        content.add_seq(unprocessed.sequence)  # Updates statistics
        content.add_trim(unprocessed.sequence, left, right)  # Updates trimming statistics
        return processed  # Returns a processed read
    except:  # If the read cannot be processed, a None is returned
        return None


def adaptor_removal(unprocessed, adaptor, content):  # Performs adaptor_removal on a given sequence and/or quality
    processed = Read()  # Initializes the resulting read
    try:
        if unprocessed.sequence[:len(adaptor):].upper() == adaptor.upper():  # Checks if the adaptor is present
            processed.sequence = unprocessed.sequence[len(adaptor)::]  # Removes the adaptor from the sequence
            if unprocessed.quality:  # Removes the corresponding qualities if there's an adaptor
                processed.quality = unprocessed.quality[len(adaptor)::]
            content.add_adaptor()  # Updates the adaptor statistics
        else:  # If there's no adaptor, the resulting read is the input read
            processed.sequence = unprocessed.sequence
            processed.quality = unprocessed.quality
        content.add_seq(unprocessed.sequence)  # Updates the statistics
        return processed  # Returns the processed read
    except:  # If the read cannot be processed, a None is returned
        return None


parameters = get_par(sys.argv)  # Cast the arguments to the parsing function

if check_par(parameters) is False:  # Checks the validity of the input arguments and exit if they're not valid
    print("Invalid arguments used. Exiting.")
    exit(1)

parameters["format"] = get_format(parameters["input"])  # Establishes the format of the input file
if parameters["format"] is False:  # If an invalid format is used, it aborts the operation
    print("Invalid file format. Exiting.")
    exit(1)

if parameters["operation"] == "trim":  # When trimming, checks if a right and left parameter has been provided
    if "trim-left" not in parameters.keys():
        parameters["trim-left"] = 0  # Sets the default value for left-trimming
    else:
        parameters["trim-left"] = int(parameters["trim-left"])  # Converts the parameter to an integer
    if "trim-right" not in parameters.keys():  # Same as before
        parameters["trim-right"] = None
    else:
        parameters["trim-right"] = int(parameters["trim-right"]) * -1

new_file = open(parameters["output"], "wt")  # Creates the output file
content = Summary()  # Initializes the statistics summary of the operation

with open(parameters["input"], "rt") as fp:  # Opens the input file
    while True:  # Allows to iterate over the file
        tag = fp.readline().rstrip()  # First line is the tag
        if not tag:  # If the tag is empty, the end of the file has been reached and the processing has been completed
            break
        sequence = fp.readline().rstrip()  # Next line is the sequence
        current_read = Read(sequence)  # Initializes a Read object with the given sequence
        if parameters["format"] == "FASTQ":  # If it's a FASTQ file, it also stores the qualities in the Read object
            fp.readline()  # Skips the "+" line
            quality = fp.readline().rstrip()
            current_read.quality = quality
        # The following lines perform the necessary operation on the read and stores the result
        if parameters["operation"] == "rc":
            processed_read = revcomp(current_read, content)
        elif parameters["operation"] == "trim":
            processed_read = trim(current_read, parameters["trim-left"], parameters["trim-right"], content)
        else:
            processed_read = adaptor_removal(current_read, parameters["adaptor"], content)

        if processed_read:  # If the read has been processed, it writes the result on the new file
            new_file.write(tag + "\n" + processed_read.sequence + "\n")
            if processed_read.quality:  # If it is a FASTQ file, the processed qualities are present
                new_file.write("+\n" + processed_read.quality + "\n")  # The processed qualities are written on the file
        else:  # If the operation could not be completed, the read is discarded and a warning is raised
            print(tag, "could not be processed.")

new_file.close()  # Closes the new file
content.report(parameters["operation"])  # Prints the summary of the operation
exit(0)
