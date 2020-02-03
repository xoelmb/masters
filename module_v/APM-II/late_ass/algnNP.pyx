## ALIGN with EDIT DISTANCE

import numpy as np

def align_edit_distance ( pattern, text ):
  vsz= len(pattern)+1
  hsz= len(text)+1
  
  dp_matrix = np.zeros( (vsz,hsz), dtype= np.int32 )

  for v in range(vsz):
    dp_matrix[v,0] = v
  for h in range(hsz):
    dp_matrix[0,h] = h

  for v in range(1,vsz):
    for h in range(1,hsz):
      dp_matrix[v,h] = min (dp_matrix[v-1,h-1] + (0 if pattern[v-1]==text[h-1] else 1), 
                            dp_matrix[v,h-1] + 1, 
                            dp_matrix[v-1,h] + 1)
  return dp_matrix


## Backtrace to generate OPTIMUM CIGAR
def backtrace_matrix ( pattern, text, dp_matrix ):
  vsz= len(pattern)+1
  hsz= len(text)+1
  
  v = vsz-1
  h = hsz-1
  cigar = []
  while v>0 and h>0:
    if dp_matrix[v,h] == dp_matrix[v-1,h] + 1:
      v -= 1
      cigar.insert(0,"D")
    elif dp_matrix[v,h] == dp_matrix[v,h-1] + 1: 
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


## MAIN FUNCTION
def align( infilename, outfilename):

  ## Opening input & output
  infile  = open(infilename)
  outfile = open(outfilename, 'w')

  pattern= infile.readline()
  text   = infile.readline()

  N=0
  while (len(pattern) and len(text) > 1):
    dp    = align_edit_distance ( pattern[1:], text[1:] )
    cigar = backtrace_matrix ( pattern[1:], text[1:], dp )
    outfile.write(str(N)+"\t")
    write_cigar ( cigar, outfile )    
    pattern= infile.readline()
    text   = infile.readline()
    N += 1
  
  infile.close()
  outfile.close()