import numpy as np
import cython

from libc.stdlib cimport malloc, free

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)

cdef int align_edit_distance ( char *pt, char *tx, int vsz, int hsz, int[:,::1] dp, char *cigar ): 
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


cdef void write_cigar( char * CIG, int pos, ofile ):
  
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


@cython.boundscheck(False)
@cython.wraparound(False)
cdef void copyString( char *in_s, char *out_s, int Sz):
  cdef int i
  for i in range(Sz):
    out_s[i] = in_s[i]
  out_s[Sz] = 0



@cython.boundscheck(False)
@cython.wraparound(False)
def align(in_filename, out_filename):

  cdef int vsz, hsz, v, h, vMAX, hMAX, vTOT, hTOT
  cdef int i, N, vPos, hPos

  ## Compute number of sequence pairs, aggregate and maximum length of sequences
  infile  = open(in_filename)
  N, vMAX, hMAX = 0, 1, 1
  vTOT, hTOT    = 0, 0
  pattern, text = infile.readline(), infile.readline()
  vsz, hsz      = len(pattern), len(text)
  while (vsz and hsz > 1):
    N = N+1
    vTOT, hTOT = vTOT+vsz, hTOT+hsz
    if (vMAX<vsz):
      vMAX = vsz
    if (hMAX<hsz):
      hMAX = hsz
    pattern, text = infile.readline(), infile.readline()
    vsz, hsz = len(pattern), len(text)

  infile.close()
  

  ## Allocate memory for sequences and cigar & read from file
  cdef int[::1] PattIdx= np.empty( N+1, dtype= np.intc )
  cdef int[::1] TextIdx= np.empty( N+1, dtype= np.intc )
  cdef int[::1] CgIdx  = np.empty( N,   dtype= np.intc )

  cdef char *ptBUFFER
  cdef char *txBUFFER
  cdef char *cgBUFFER

  ptBUFFER = <char *> malloc(sizeof(char)*vTOT)
  txBUFFER = <char *> malloc(sizeof(char)*hTOT)
  cgBUFFER = <char *> malloc(sizeof(char)*(vTOT+hTOT+N))

  infile        = open(in_filename)

  pattern, text = infile.readline(), infile.readline()
  vsz, hsz      = len(pattern), len(text)
  vPos, hPos    = 0, 0
  for i in range(N):
    copyString( pattern[1:].encode(), ptBUFFER+vPos, vsz-1)
    copyString( text[1:].encode(),    txBUFFER+hPos, hsz-1)
    PattIdx[i], TextIdx[i] = vPos, hPos
    vPos, hPos  = vPos + vsz, hPos + hsz
    pattern, text = infile.readline(), infile.readline()
    vsz, hsz      = len(pattern), len(text)

  PattIdx[N], TextIdx[N] = vPos, hPos

  if (vPos<>vTOT or hPos<>hTOT):  # sanity check
    print("ERROR") 
  
  infile.close()



  ## Allocate memory for Dynamic Programming Matrix and perform the N alignments

  cdef int[:,::1] dp = np.empty( (vMAX,hMAX), dtype= np.intc )

  for v in range(vMAX):
    dp[v,0] = v

  for h in range(hMAX):
    dp[0,h] = h

  for i in range(N):
    vPos, hPos = PattIdx[i], TextIdx[i]
    vsz,  hsz  = PattIdx[i+1]-vPos, TextIdx[i+1]-hPos
    CgIdx[i] = align_edit_distance( ptBUFFER+vPos, txBUFFER+hPos, vsz, hsz, dp, cgBUFFER+vPos+hPos+i )

  free(ptBUFFER) ## free the memory allocated previously
  free(txBUFFER)



  ## Write cigars to file and then close file and free memory
  outfile = open(out_filename, 'w')

  for i in range(N):
    outfile.write ( str(i) + "\t" )
    vPos, hPos = PattIdx[i], TextIdx[i]
    write_cigar( cgBUFFER+vPos+hPos+i, CgIdx[i], outfile )

  outfile.close()
  free(cgBUFFER)
