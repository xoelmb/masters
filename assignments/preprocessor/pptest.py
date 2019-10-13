from typing import Dict, Any


def get_par(args):
    parameters ={}
    for i in range(len(args)):
        if args[i][0:2:] == "--":
            parameters[args[i][2::]] = args[i+1]
    return parameters


def check_par(parameters):

    print("Cal fer una funciò que comprobi que els parameters estan bé introduits.")

    return True




test_arguments=["name.py", "--input", "input.fasta", "--output", "output_file.fa", "--operation", "rc"]

parameters = get_par(test_arguments)

print(parameters)

if check_par(parameters)==False:
    print("Invalid arguments used. Exiting.")
    quit()

with open(parameters["input"], "r") as fp:
    no_line = 0
    for line in fp:
        no_line += 1
        print("Line %d: %s" % (no_line,line))