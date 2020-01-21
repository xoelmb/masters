def edit_distance_dp(pattern, text):
    # Init
    dp_matrix = [[0 for _ in range(len(text) + 1)] for _ in range(len(pattern) + 1)]
    for v in range(len(pattern) + 1):
        dp_matrix[v][0] = v
    for h in range(len(text) + 1):
        dp_matrix[0][h] = h
    # Compute DP Matrix
    for h in range(1, len(text) + 1):
        for v in range(1, len(pattern) + 1):
            dp_matrix[v][h] = min(
                dp_matrix[v - 1][h - 1] +
                (0 if pattern[v - 1] == text[h - 1] else 1),
                dp_matrix[v][h - 1] + 1,
                dp_matrix[v - 1][h] + 1)

    return dp_matrix


def backtrace_matrix(pattern,text,dp_matrix):
    v = len(pattern)
    h = len(text)
    cigar = []
    while v>0 and h>0:
        if dp_matrix[v][h] == dp_matrix[v-1][h] + 1:
            v -= 1
            cigar.insert(0,"D")
        elif dp_matrix[v][h] == dp_matrix[v][h-1] + 1:
            h -= 1
            cigar.insert(0,"I")
        else:
            v -= 1
            h -= 1
            if pattern[v] == text[h]:
                cigar.insert(0,"M")
            else:
                cigar.insert(0,"X")

    if v>0:
        for _ in range(v): cigar.insert(0,"D")
    if h>0:
        for _ in range(h): cigar.insert(0,"I")
    return cigar

# Compute edit distance
dp_matrix = edit_distance_dp("GATTACA","GGACTCA")
# Print matrix
# [0, 1, 2, 3, 4, 5, 6, 7]
# [1, 0, 1, 2, 3, 4, 5, 6]
# [2, 1, 1, 1, 2, 3, 4, 5]
# [3, 2, 2, 2, 2, 2, 3, 4]
# [4, 3, 3, 3, 3, 2, 3, 4]
# [5, 4, 4, 3, 4, 3, 3, 3]
# [6, 5, 5, 4, 3, 4, 3, 4]
# [7, 6, 6, 5, 4, 4, 4, 3]
print_dp_matrix(dp_matrix)
# Prints "(2, ['I', 'M', 'M', 'M', 'M', 'D', 'M', 'M'])"
print(backtrace_matrix("GATTACA","GGACTCA",dp_matrix))