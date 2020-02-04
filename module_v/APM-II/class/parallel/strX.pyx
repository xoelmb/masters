# This code implements the simulation of the movement of a string
#  using the numerical method of finite differences

import math
# import numpy as np
import cython
from libc.stdlib cimport malloc
from cython.parallel import prange

cpdef void run( int X, int T ):
  cdef int t
  cdef float L= 0.345678
  cdef float *U1, *U2, *Uout
  cdef int limit = X + 1
  U1 = <float *> malloc(sizeof(float) * limit)
  U2 = <float *> malloc(sizeof(float) * limit)
  Uout = <float *> malloc(sizeof(float) * limit)

  # U1  = np.zeros(X+1, dtype=np.float32)
  # U2  = np.zeros(X+1, dtype=np.float32)
  # Uout= np.zeros(X+1, dtype=np.float32)

  print("String motion: X=", X, " and T= ", T)

  init ( U1, U2, X, T )
 
  for t in range(T):
    evolve( U1, U2, Uout, X, L )
    U1,U2,Uout = Uout,U1,U2

  print("CheckSum = ", checkSUM( U1, X ))


@cython.wraparound(False)
@cython.boundscheck(False)
cdef evolve( float * U1, float * U2,
  float * Uout, int X, float L):
  cdef int x
  cdef float L2 = 2.0*(1.0-L)
  for x in range(1,X):
    Uout[x] = L2*U1[x] + L*(U1[x+1]+U1[x-1]) - U2[x]

@cython.wraparound(False)
@cython.boundscheck(False)
cdef float checkSUM ( float * In, int X ):
  cdef float S= 0
  cdef int x
  for x in range(1,X):
    S = S + In[x]
  return S

@cython.wraparound(False)
@cython.boundscheck(False)
cdef init ( float * U1, float * U2, int X, int T ):
  cdef int x
  U1[0] = U2[0] = 0.0
  U1[X] = U2[X] = 0.0
  cdef float factor2 = math.pi / X
  cdef float factor1 = math.cos(math.pi / (T+1))
  for x in range(1,X):
    U2[x]= math.sin(x * factor2)
    U1[x]= U2[x] * factor1
