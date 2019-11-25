# 1.a works
def combine(string1, string2):
    merge = ""
    min_l = min(len(string1),len(string2))
    for i in range(min_l):
        merge = merge + string1[i] + string2[i]
    if len(string1) > min_l:
        merge = merge + string1[min_l::]
    if len(string2) > min_l:
        merge = merge + string2[min_l::]
    return merge

print(combine("AAA", "GGGGG"))
print(combine("GGGGG","AAA"))


# 1.b works
def combine_recursive(string1, string2, merge=""):
    if len(string1) == 0:
        return merge + string2
    if len(string2) == 0:
        return merge + string1
    merge = merge + string1[0] + string2[0]
    return combine_recursive(string1[1::], string2[1::], merge)


print(combine_recursive("AAA", "GGGGG"))
print(combine_recursive("GGGGG","AAA"))


# 1.c works
def combine_divide_conquer(string1, string2):
    if len(string1) == 1 or len(string2) == 1:
        return string1+string2
    else:
        middle = len(string1)//2
        lefties = combine_divide_conquer(string1[:middle:], string2[:middle:])
        righties = combine_divide_conquer(string1[middle:], string2[middle::])
        return lefties+righties


print(combine_divide_conquer("AAAAA", "GGGGG")) # Prints "AGAGAGAGAG"
print(combine_divide_conquer("GGGGG","AAAAA")) # Prints "GAGAGAGAGA"
print(combine_divide_conquer("ACGTA","GGCCA")) # Prints "AGCGGCTCAA"


# 1.d works
def combine_list(slist):
    merge = ""
    maxl = None
    for string in slist:
        if not maxl:
            maxl = len(string)
        elif len(string) > maxl:
            maxl = len(string)
    for i in range(maxl):
        for string in slist:
            if len(string) > i:
                merge = merge + string[i]
    return merge


print(combine_list(["AA", "GGGGG", "TTTTTT"]))



# 2.a works
def fastq_count_masked_bases(file_path):
    counter = 0
    with open(file_path, "rt") as f:
        while True:
            tag = f.readline()
            if not tag: break
            seq = f.readline().rstrip()
            f.readline()
            f.readline()
            for base in seq:
                if base.islower():
                    counter += 1
        f.close()
    return counter


print(fastq_count_masked_bases("sample.fastq"))


# 2.b works
def fastq_isolated_masked_chunks(input_fastq_path, output__fastq_path):
    output = open(output__fastq_path, "wt")
    with open(input_fastq_path, "rt") as f:
        while True:
            tag = f.readline().rstrip()
            if not tag: break
            seq = f.readline().rstrip()
            counter = 1
            plus = f.readline()
            quals = f.readline()
            chunk = ""
            chunk_q = ""
            for i in range(len(seq)):
                if seq[i].islower():
                    detected = True
                    chunk = chunk + seq[i]
                    chunk_q = chunk_q + quals[i]
                else:
                    if detected:
                        detected = False
                        output.write(tag+"."+str(counter)+"\n"+chunk+"\n"+plus+chunk_q+"\n")
                        counter += 1
                        chunk = ""
                        chunk_q = ""
            if detected is True:
                output.write(tag + "." + str(counter) + "\n" + chunk + "\n" + plus + chunk_q + "\n")
        f.close()
    output.close()


fastq_isolated_masked_chunks("sample.fastq", "sample.masked.chunks.fastq")



# 3.a works
cat mbio.sample.sam | grep -vE "^@" | head -n 500 | tail -n 1


# 3.b works
awk '{print $10}' mbio.sample.sam | fold -w 1 | sort | uniq -c | grep -E "[a-z]" | sort -rn | head -n 1


# 3.c NOT FINISHED
awk 'NR%4==1{a='



# 4.a. works
def student_final_grade(students_grades,student_id):
    if not student_id in students_grades.keys():
        print("Student not found.")
        return
    addition= 0
    count = 0
    for assignment in students_grades[student_id]:
        count +=1
        addition += float(assignment[1])
    print("Student's final grade is:", addition/count)


students_grades = {
    "5214784": [("boxes", 10.0), ("fastx", 8.0), ("gameOfLive", 10.0)],
    "2365489": [("boxes", 8.0), ("gameOfLive", 10.0)],
    "1371629": [("gameOfLive", 10.0), ("fastx", 3.0), ("boxes", 9.5)]
}
student_final_grade(students_grades,"1371629") # Prints "Student's final grade is: 7.5"
student_final_grade(students_grades,"9999999") # Prints "Student not found"


# 4.b works
def student_final_grade(students_grades,student_id):
    if not student_id in students_grades.keys():
        print("Student not found.")
        return
    scores = {}
    for student in students_grades.keys():
        for assignment in students_grades[student]:
            if not assignment[0] in scores.keys():
                scores[assignment[0]] = []
            scores[assignment[0]].append(float(assignment[1]))
    mean_scores = {}
    for assignment in scores.keys():
        mean_scores[assignment] = sum(scores[assignment]) / len(scores[assignment])
    addition= 0
    count = 0
    for assignment in students_grades[student_id]:
        print("Student's grade on "+assignment[0]+": "+str(assignment[1])+".\n\tClass average: "+str(mean_scores[assignment[0]]))
        count +=1
        addition += float(assignment[1])
    print("Student's final grade is:", addition/count)


student_final_grade(students_grades,"1371629")


# 5. NOT RECURSIVE, NOT FINISHED
# def is_combination(a,b,c):
#     p1 = 0
#     p2 = 0
#     p3 = 0
#     result = True
#     while p3 < len(c) and p1 < len(a) and p2 < len(b):
#         if c[p3] == a[p1]:
#             p1 += 1
#             p3 += 1
#         elif c[p3] == b[p2]:
#             p2 += 1
#             p3 += 1
#         else:
#             print(a[p1], b[p2], c[p3])
#             return False
#
#     if p1 < len(a):
#         print(c[p3::])
#         print(a[p1::])
#         if c[p3::] != a[p1::]:
#             return False
#         else:
#             return True
#     if p2 < len(b):
#         print(c[p3::])
#         print(b[p2::])
#         if c[p3::] != b[p2::]:
#             return False
#         else:
#             return False
#
#
# print(is_combination("AAA","GGGG","AAGAGGG")) # True
# # print(is_combination("AAA","GGGG","AAGAGG")) # False
# print(is_combination("TATA","AGAG","TAGAAGTA")) # True


def is_combination(a, b, c):
    if len(a) == 0:
        return b == c
    elif len(b) == 0:
        return a == c
    else:
        if a[0] == c[0]:
            return is_combination(a[1::],b,c[1::])
        elif b[0] == c[0]:
            return is_combination(a, b[1::], c[1::])
        else:
            return False

print(is_combination("AAA","GGGG","AAGAGGG")) # True
print(is_combination("AAA","GGGG","AAGAGG")) # False
print(is_combination("TATA","AGAG","TAGAAGTA")) # True
