import numpy as np
import cython
from cython.parallel import prange

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)

cdef int align_edit_distance ( char *pt, char *tx, int vsz, int hsz, int[:,::1] dp, char[::1] cigar ) nogil: 
  cdef int v, h, c
  for v in range(1,vsz):
    for h in range(1,hsz):
      dp[v,h] = min (dp[v-1,h-1] + (0 if pt[v-1]==tx[h-1] else 1), 
                     dp[  v,h-1] + 1, 
                     dp[v-1,  h] + 1)

  v, h, c = vsz-1, hsz-1, 0
  while v>0 and h>0:
    if dp[v,h] == dp[v-1,h] + 1:
      v -= 1
      cigar[c]= 3 # "D"
    elif dp[v,h] == dp[v,h-1] + 1: 
      h -= 1
      cigar[c]= 2 # "I"
    else:
      v -= 1
      h -= 1
      if pt[v] == tx[h]:
        cigar[c]= 0 # "M"
      else:
        cigar[c]= 1 # "X"
    c=c+1

  if v>0:
    for _ in range(v): 
      cigar[c]=3 # "D"
      c=c+1
  if h>0:
    for _ in range(h):
      cigar[c]=2 # "I"
      c=c+1

  return c


cdef void write_cigar( char[::1] CIG, int pos, ofile ):
  
  cdef int  count= 0, i
  cdef char last=4, v
  Translate = ['M','X','I','D','A']

  for i in range(pos,0,-1):
    v = CIG[i-1]
    if v == last:
      count += 1
    else:
      if count != 0:
        ofile.write(str(count)+Translate[last])
      last = v
      count=1

  if count != 0:
    ofile.write(str(count)+Translate[last])

  ofile.write("\n")


def align(in_filename, out_filename):

  cdef int vsz, hsz, v, h
  cdef int i, N
  cdef char *pt
  cdef char *tx

  ## Opening input & output
  infile  = open(in_filename)

  # Generate work from file into lists
  P, T, C = [], [], []

  N=0
  vMAX, hMAX= 1, 1

  pattern= infile.readline()
  text   = infile.readline()
  vsz = len(pattern)
  hsz = len(text)

  while (vsz and hsz > 1):
    P.append(pattern[1:].encode())
    T.append(text[1:].encode())
    C.append(np.empty ( vsz+hsz-1, dtype= np.uint8 ))
    if (vMAX<vsz):
      vMAX = vsz
    if (hMAX<hsz):
      hMAX = hsz
    pattern= infile.readline()
    text   = infile.readline()
    vsz    = len(pattern)
    hsz    = len(text)
    N += 1
  
  infile.close()


  cdef int[:,::1] dp = np.empty( (vMAX,hMAX), dtype= np.intc )
  cdef int[::1]   Out= np.empty( N, dtype= np.intc )

  for v in range(vMAX):
    dp[v,0] = v

  for h in range(hMAX):
    dp[0,h] = h

  for i in range(N):
    pt, tx, cg = P[i], T[i], C[i]
    vsz, hsz = len(pt), len(tx)
    Out[i] = align_edit_distance( pt, tx, vsz, hsz, dp, cg )


  outfile = open(out_filename, 'w')

  for i in range(N):
    outfile.write ( str(i) + "\t" )
    write_cigar( C[i], Out[i], outfile )

  outfile.close()
