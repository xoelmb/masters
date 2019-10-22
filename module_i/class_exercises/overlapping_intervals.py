import sys

#Store the positions of both sequences as two different lists.

seq1 = [int(sys.argv[1]),int(sys.argv[2])]
seq2 = [int(sys.argv[3]),int(sys.argv[4])]


#To check if the sequences are overlapping, we only need to check if the space they occupy
#{i.e. (seq1[1]-seq1[0])+(seq2[1]-seq2[0]) } is larger than the distance from the closest
#point to the furthest point {i.e. max([seq1[1],seq2[1]])-min([seq1[0],seq2[0]]) }

if ((seq1[1]-seq1[0])+(seq2[1]-seq2[0]))>=(max([seq1[1],seq2[1]])-min([seq1[0],seq2[0]])):
    print("The sequences are overlapping.")

else:
    print("The sequences are not overlapping.")
