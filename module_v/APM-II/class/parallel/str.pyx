# This code implements the simulation of the movement of a string
#  using the numerical method of finite differences

import math
import numpy as np
import cython

@cython.wraparound(False)
@cython.boundscheck(False)

def run( int X, int T ):
  cdef int   t, x
  cdef float S, L= 0.345678
  cdef float [:,::1] U= np.zeros((X+1,T+2), dtype=np.float32)

  print("String motion: X=", X, " and T= ", T)

  # initialize positions of matrix U
  for x in range (1,X):
    U[x][0] =           math.sin( x * math.pi / X )
    U[x][1] = U[x][0] * math.cos( math.pi / (T+1) )
 
  # compute simulation
  for t in range(T):
    for x in range(1,X):
      U[x][t+2] = 2.0*(1.0-L)*U[x][t+1] + L*(U[x+1][t+1]+U[x-1][t+1]) - U[x][t]

  # compute checksum
  S= 0
  for x in range(1,X):
    S = S + U[x][T+1]

  print("CheckSum = ", S)
