# The script below codes for a FASTX preprocessor that can reverse-complement, trim and remove adaptors for both FASTA
# and FASTQ files. The code has been designed to be versatile, modular and to be used even if the input arguments are
# slightly messy. For example, it can not only perform trimming if both left and right parameters are established, but
# it can also perform right- or left-only trimming to sequences. Due to that, some extra code and variables had to be
# written, but I think the trade-off is worth it since it makes the script more robust overall.
# The use of classes allowed me to create quite flexible functions and to record and update the statistics along the
# script with the use of only one object and its defined methods.


import re
import sys


class Read:  # Class used to store sequence and quality of a given read
    def __init__(self, seq=None, qual=None):
        self.sequence = seq
        self.quality = qual


class Summary:  # Class used to store different statistics of the whole operation
    def __init__(self):
        self.bases_dic = {"A": 0, "C": 0, "G": 0, "T": 0, "N": 0}
        self.bases_total = 0
        self.seqs = 0
        self.adaptors = 0
        self.trim_dic = {"A": 0, "C": 0, "G": 0, "T": 0, "N": 0}
        self.trim_total = 0

    def add_seq(self, seq):  # Function to update statistics on the analysis when a sequence is processed
        self.seqs += 1
        for base in seq[::].upper():
            if base in self.bases_dic.keys():
                self.bases_dic[base] += 1
            self.bases_total += 1

    def add_trim(self, seq, left, right, total):  # Update statistics when a trim operation is performed
        seq_left = ""
        seq_right = ""
        if len(seq) > total:
            if left != 0:
                seq_left = seq[:left:]
            if right is not None:
                seq_right = seq[right::]
            removed = seq_left + seq_right
        else:
            removed = seq
        for base in removed[::].upper():
            if base in self.trim_dic.keys():
                self.trim_dic[base] += 1
            self.trim_total += 1

    def add_adaptor(self):  # Update statistics when a adaptor is found
        self.adaptors += 1

    def report(self, mode):  # Function to print statistics depending on the operation performed
        print("Summary:\n" + (len(str(self.bases_total)) - len(str(self.seqs))) * " " + str(self.seqs),
              "reads processed\n" + str(self.bases_total), "bases processed (",
              end="")
        for base in ["A", "C", "G", "T", "N"]:
            print(str(int(self.bases_dic[base] / self.bases_total * 100)) + "%", base, end="")
            if base != "N":
                print(", ", end="")
            else:
                print(")")
        if mode == "trim":
            print((len(str(self.bases_total)) - len(str(self.trim_total))) * " " + str(self.trim_total),
                  "bases trimmed (", end="")
            for base in ["A", "C", "G", "T", "N"]:
                print(str(int(self.trim_dic[base] / self.trim_total * 100)) + "%", base, end="")
                if base != "N":
                    print(", ", end="")
                else:
                    print(")")
        elif mode == "adaptor_removal":
            print((len(str(self.bases_total)) - len(str(self.adaptors))) * " " + str(self.adaptors) + " adaptors found")


def get_par(args):  # Function to parse the arguments used by the user
    pars = {}  # Dictionary used to store the parameters
    last = ""  # Initialize a variable that stores the last value added to the dictionary
    for i in range(1, len(args)):  # Iterate over arguments, except for the first one (name of file)
        if args[i][0:2:] == "--" and i != len(args) - 1:  # Checks if the argument is a parameter and not the last one
            pars[args[i][2::]] = args[i + 1]  # Stores the next argument as the value of a given parameter
            last = args[i + 1]  # Updates the last value stored
        elif args[i] != last:  # If an argument has not been preceded by a "--parameter", it's ignored
            print(args[i] + ": missing operator")
    return pars  # Returns the whole dictionary of parameters


def check_par(pars):  # Checks if the provided arguments are valid and converts trimming values if necessary
    # Checks if the minimum arguments are present
    if "input" not in pars.keys() or "output" not in pars.keys() or "operation" not in pars.keys():
        print("The minimum parameters are --input, --output and --operation.")
        return False
    try:  # Checks if the input file can be opened
        f = open(pars["input"], "rt")
        f.close()
    except FileNotFoundError:
        print("Input file was not found.")
        return False
    if pars["operation"] == "rc":  # If reverse-complement has been selected, no further checks are required
        return True
    elif pars["operation"] == "adaptor_removal":  # If adaptor_removal, checks if there's a valid adaptor
        if "adaptor" not in pars.keys():
            print("adaptor_removal requires an adaptor sequence.")
            return False
        if re.search(r'\A[ACGTNacgtn]+\Z', pars["adaptor"]):
            return True
        else:
            print("The adaptor sequence provided is not valid (only ACGTN/acgtn strings).")
            return False
    elif pars["operation"] == "trim":  # If trim, checks and converts the values to integers
        defaults = {"trim-left": 0, "trim-right": None}  # Default values if a trim value has not been provided
        multiplier = {"trim-left": 1, "trim-right": -1}  # Allows to convert the value to a valid index for slicing
        pars["trim-total"] = 0  # Stores the total number of bases to be trimmed
        for side in ["trim-left", "trim-right"]:  # Checks both left and right
            if side not in pars.keys():  # If the parameter has not been provided
                pars[side] = defaults[side]  # Sets that parameter to its default
            else:  # If the argument has been provided
                if pars[side].isdigit():  # Checks if it's a positive integer
                    pars["trim-total"] += int(pars[side])  # Adds the parameter to the count of bases
                    pars[side] = int(pars[side]) * multiplier[side]  # Adapts it to a valid integer index
                else:  # When an invalid value is provided, it returns False (the operation will be aborted)
                    print("Invalid", side, "argument. Only positive integers can be used.")
                    return False
        if pars["trim-total"] > 0:
            # Only if the user provides at least one valid and no invalid trimming values, it returns True
            return True
        else:  # When the user provides no trimming values and trim is selected
            print("Missing trimming arguments.")
            return False
    else:  # If the operation is not one of those three, it returns False
        print("Invalid operation:", pars["operation"] + ".\n\trc, trim or adaptor_removal is expected.")
        return False


def get_format(input_file):  # Function to get the format of the input file
    file_format = False
    with open(input_file, "r") as file:
        line = file.readline()
        if line[0] == ">":
            file_format = "FASTA"
        elif line[0] == "@":
            file_format = "FASTQ"
    return file_format


def revcomp(unprocessed, stats):  # Performs reverse-complement on a given sequence and quality if needed
    comp_dic = {"A": "T", "C": "G", "G": "C", "T": "A", "N": "N", "a": "t", "c": "g", "g": "c", "t": "a", "n": "n"}
    processed = Read()  # Initializes the resulting read
    try:
        processed.sequence = "".join(comp_dic[base] for base in unprocessed.sequence[::-1])  # Revcom the sequence
        if unprocessed.quality:  # Reverses the qualities if the read contains any
            processed.quality = "".join(unprocessed.quality[::-1])
        stats.add_seq(unprocessed.sequence)  # Updates the statistics
        return processed  # Returns a processed read
    except KeyError:  # If the read cannot be processed (e.g. invalid characters used), a None is returned
        return None


def trim(unprocessed, left, right, total, stats):  # Performs trimming on a given sequence and quality if needed
    processed = Read()  # Initializes the resulting read
    if len(unprocessed.sequence) > total:
        processed.sequence = unprocessed.sequence[left:right:]  # Trims the sequence
        if unprocessed.quality:  # Trims the qualities if the read contains any
            processed.quality = unprocessed.quality[left:right:]
    stats.add_seq(unprocessed.sequence)  # Updates statistics
    stats.add_trim(unprocessed.sequence, left, right, total)  # Updates trimming statistics
    return processed  # Returns a processed read


def adaptor_removal(unprocessed, adaptor, stats):  # Performs adaptor_removal on a given sequence and/or quality
    processed = Read()  # Initializes the resulting read
    if unprocessed.sequence[:len(adaptor):].upper() == adaptor.upper():  # Checks if the adaptor is present
        processed.sequence = unprocessed.sequence[len(adaptor)::]  # Stores the sequence without the adaptor
        if unprocessed.quality:  # Removes the corresponding qualities if there's an adaptor
            processed.quality = unprocessed.quality[len(adaptor)::]
        stats.add_adaptor()  # Updates the adaptor statistics
    else:  # If there's no adaptor, the resulting read is the input read
        processed = unprocessed
    stats.add_seq(unprocessed.sequence)  # Updates the statistics
    return processed  # Returns the processed read


parameters = get_par(sys.argv)  # Cast the arguments to the parsing function

if check_par(parameters) is False:  # Checks the validity of the input arguments and exit if they're not valid
    print("Invalid arguments used. Exiting.")
    exit(1)

parameters["format"] = get_format(parameters["input"])  # Establishes the format of the input file
if parameters["format"] is False:  # If an invalid format is used, it aborts the operation
    print("Invalid file format. Exiting.")
    exit(1)

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
            processed_read = trim(current_read, parameters["trim-left"], parameters["trim-right"], parameters["trim-total"], content)
        elif parameters["operation"] == "adaptor_removal":
            processed_read = adaptor_removal(current_read, parameters["adaptor"], content)
        else:
            processed_read = None

        if processed_read:  # If the read has been processed, it writes the result on the new file
            if processed_read.sequence:  # Only if the sequence has not been completely trimmed/deleted
                new_file.write(tag + "\n" + processed_read.sequence + "\n")
                if processed_read.quality:  # If it is a FASTQ file, the processed qualities are present
                    new_file.write("+\n" + processed_read.quality + "\n")  # Writes processed qualities on the file
        else:  # If the operation could not be completed, the read is discarded and a warning is raised
            print(tag, "could not be processed.")

new_file.close()  # Closes the new file
final_print = {"rc": "reversed-complemented", "adaptor_removal": "processed", "trim": "hard-trimmed"}
print("\nFile '" + parameters["input"] + "' has been successfully %s " % final_print[parameters["operation"]] + "('" + parameters["output"] + "')")
content.report(parameters["operation"])  # Prints the summary of the operation
exit(0)