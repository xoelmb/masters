# # 1.
# def add_to(n, m):
#     for i in range(n):
#         for j in range(n):
#             for k in range(n):
#                 if i + j + k == m:
#                     print(i, "+", j, "+", k, "=", 150)
#
#
# add_to(100, 150)


# # 2.a
# def get_divisors(n):
#     divs = []
#     for i in range(1, n+1):
#         if n % i == 0:
#             divs.append(i)
#     return divs
#
#
# print(get_divisors(100))
#
#
# # 2.b
# def is_perfect(n):
#     total_sum = 0
#     for i in get_divisors(n):
#         if i != n:
#             total_sum += i
#     if total_sum == n:
#         return True
#     else:
#         return False
#
#
# print(is_perfect(6))
#
#
# # 2.c
# def range_is_perfect(n=1, m=1000):
#     perfects = []
#     for i in range(n, m+1):
#         if is_perfect(i):
#             perfects.append(i)
#     return perfects
#
#
# print(range_is_perfect())


# 3.a
# def fastq_to_fasta(fastq):
#     fasta = fastq.replace(".fastq", ".fasta")
#     fa = open(fasta, "wt")
#     with open(fastq, "rt") as fq:
#         while True:
#             tag = fq.readline()
#             if not tag:
#                 break
#             seq = fq.readline()
#             fq.readline()
#             fq.readline()
#             fa.write(">"+tag[1::]+seq)
#         fq.close()
#     fa.close()
#     return fasta
#
#
# fastq_to_fasta("sample.fastq")


# # 3.b
# def fastq_split(fastq):
#     split_fq = open(fastq.replace('.fastq','.split.fastq'), "wt")
#     with open(fastq, "rt") as fq:
#         while True:
#             tag = fq.readline()
#             if not tag: break
#             seq = fq.readline()
#             fq.readline()
#             qual = fq.readline()
#             split_fq.write(tag+ seq[:len(seq)//2:] + "\n+\n" + qual[:len(qual)//2:] + "\n" + tag+ seq[len(seq)//2::]+ "+\n" + qual[len(qual)//2::])
#         fq.close()
#     split_fq.close()
#
#
# fastq_split("sample.fastq")
#

# # 4.a,b
# import re
# # import regex as re
#
#
# def find_TATA(seq):
#     match = re.compile(r'(T+A+T+A+)')
#     for m in match.finditer(seq):
#         print("Found", m.group(0), "at", m.start())
#
#
# find_TATA("TAAATAATATTTTAAATTATATTAAGTCGTAGCTA")
#

# def find_TATA(seq):
#     match = re.findall(r'(T+A+T+A+)', seq, overlapped=True)
#     for m in match:
#         print(m)
#
#
# find_TATA("TAAATAATATTTTAAATTATATTAAGTCGTAGCTA")


# 6.a
# def rem_adaptor(seq, adapt):
#     if seq[:len(adapt):] == adapt:
#         return seq[len(adapt)::]
#     else:
#         return seq
#
#
# print(rem_adaptor("ACGTACGTACGT", "ACG"))


# 6.b
# def rem_adaptor(seq, adapt):
#     mismatches = 0
#     for i in range(len(adapt)):
#         if seq[i] != adapt[i]:
#             mismatches += 1
#             if mismatches > 1:
#                 return seq
#     return seq[len(adapt)::]
#
#
# print(rem_adaptor("ACGTACGTACGT", "TCG"))


# 7.a
# def iter_cond(string):
#     last_cha = ""
#     condensed = ""
#     for i in range(len(string)):
#         if string[i] != last_cha:
#             condensed += string[i]
#         last_cha = string[i]
#     return condensed
#
#
# print(iter_cond("AAAGCTTTTFGGGDHHHSKK"))
#
#
# # 7.b
# def rec_cond(string, prev=""):
#     if len(string) == 0:
#         return ""
#     else:
#         if prev == string[0]:
#             return rec_cond(string[1:], prev)
#         else:
#             return string[0] + rec_cond(string[1:], string[0])
#
#
# print(rec_cond("AAAGCTTTTFGGGDHHHSKK"))
#
#
# # 7.c
# def dac_cond(string):
#     if len(string) == 1:
#         return string
#     else:
#         left = dac_cond(string[:len(string)//2:])
#         right = dac_cond(string[len(string)//2::])
#         if left[-1] != right[0]:
#             left += right
#         else:
#             left += right[1::]
#     return left
#
# print(dac_cond("AAAGCTTTTFGGGDHHHSKK"))
