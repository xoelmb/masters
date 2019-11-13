import matplotlib.pyplot as plt
dict_nuc = {}
with open("../preprocessor/mbio.sample.fastq", "rt") as f:
    while True:
        tag = f.readline()
        if not tag: break
        sequence = f.readline().rstrip()
