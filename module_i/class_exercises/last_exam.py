def is_palindrome(seq):
    if len(seq) % 2 == 0:
        if seq[:len(seq)/2:] == seq[len(seq)/2::-1]:
            return True
        else:
            return False
    else:
        if seq[:len(seq)%2:] == seq[len(seq)%2+1::-1]:
            return True
        else:
            return False

def make_palindromes(k):
    collection = []# do the mirror thing
    return collection


def count(palindromes, k):


