## ALIGN with EDIT DISTANCE

cdef list align_edit_distance ( char *pattern, char *text ):
  cdef int v, h
  cdef list dp_matrix= [[0 for _ in range(len(text)+1)] for _ in range(len(pattern)+1)]
  for v in range(len(pattern)+1):
    dp_matrix[v][0] = v
  for h in range(len(text)+1):
    dp_matrix[0][h] = h

  for h in range(1,len(text)+1):
    for v in range(1,len(pattern)+1):
      dp_matrix[v][h] = min (dp_matrix[v-1][h-1] + (0 if pattern[v-1]==text[h-1] else 1), 
                             dp_matrix [v] [h-1] + 1, 
                             dp_matrix[v-1] [h]  + 1)
  return dp_matrix


## Backtrace to generate OPTIMUM CIGAR
def backtrace_matrix ( pattern, text, dp_matrix ):
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

def write_cigar( C, ofile ):
  last="A"
  count=0
  ofile.write("CIGAR=")
  for v in C:
    if v == last:
      count += 1
    else:
      if count != 0:
        ofile.write(str(count)+last)
      last=v
      count=1

  if count != 0:
    ofile.write(str(count)+last)

  ofile.write("\n")
  return

def align(in_filename, out_filename):
  """
  in_filename:  input file containing pairs of sequences to align
  out_filename: output file with alignment cigars for input pairs
  """

  ## Opening input & output
  infile  = open(in_filename)
  outfile = open(out_filename, 'w')

  pattern= infile.readline()
  text   = infile.readline()

  N=0
  while (len(pattern) and len(text) > 1):
    dp    = align_edit_distance ( pattern[1:].encode('utf-8'), text[1:].encode('utf-8') )
    cigar = backtrace_matrix ( pattern[1:], text[1:], dp )
    outfile.write(str(N)+"\t")
    write_cigar ( cigar, outfile )    
    pattern= infile.readline()
    text   = infile.readline()
    N += 1
  
  infile.close()
  outfile.close()
