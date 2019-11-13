# # Exercise 1
# for i in range(1, 101):
#     for j in range(1, 101):
#         for k in range(1, 101):
#             if i + j + k == 150:
#                 print(str(i) + "+" + str(j) + "+" + str(k) + "=150")
#
#
# # Exercise 2
#
#
# # Exercise 3
# def to_fasta(input_file):
#     o = open(input_file.replace('fastq', 'fasta'), "wt")
#     with open(input_file, "rt") as f:
#         while True:
#             tag = f.readline()
#             if not tag: break
#             seq = f.readline()
#             o.write(tag.replace("@", ">") + seq)
#             f.readline()
#             f.readline()
#
#     o.close()
#
#
# def fastq_split(input_file):
#     o = open(input_file.replace('.fastq','.split.fastq'), "wt")
#     with open(input_file, "rt") as f:
#         while True:
#             tag = f.readline()
#             if not tag: break
#             seq = f.readline()
#             f.readline()
#             qual = f.readline()
#             o.write(tag+ seq[:len(seq)//2:] + "\n+\n" + qual[:len(qual)//2:] + "\n" + tag+ seq[len(seq)//2::]+ "+\n" + qual[len(qual)//2::])
#
#     o.close()
#
#
# to_fasta("mbio.sample.fastq")
# fastq_split("mbio.sample.fastq")
#
# Exercise 7


def iter_cond(string):
    last_cha = ""
    condensed = ""
    for i in range(len(string)):
        if string[i] != last_cha:
            condensed += string[i]
        last_cha = string[i]
    return condensed


print(iter_cond("AAAGCTTTTFGGGDHHHSKK"))


def rec_cond(string, prev):
    if len(string) == 0:
        return ""
    else:
        if prev == string[0]:
            return rec_cond(string[1:], prev)
        else:
            return string[0] + rec_cond(string[1:], string[0])


print(rec_cond("AAAGCTTTTFGGGDHHHSKK", ""))


def dac_cond(string):
    if len(string) == 1:
        return string
    else:
        left = dac_cond(string[:len(string)//2:])
        right = dac_cond(string[len(string)//2::])
        if left[-1] != right[0]:
            left += right
        else:
            left += right[1::]
    return left

print(dac_cond("AAAGCTTTTFGGGDHHHSKK"))
