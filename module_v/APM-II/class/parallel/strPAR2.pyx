import cython

from cython.parallel import prange
from libc.stdlib cimport malloc, free
from libc.math cimport sin, cos, pi


def run( int X, int T ):
  cdef int t
  cdef float L= 0.12345678, S
  cdef float *U1
  cdef float *U2
  cdef float *Uout

  print("String motion: X=", X, 
    " and T= ", T)

  with nogil: 
    U1  = <float *> malloc( (X+1) * sizeof(float))
    U2  = <float *> malloc( (X+1) * sizeof(float))
    Uout= <float *> malloc( (X+1) * sizeof(float))
    init ( U1, U2, X, T )
    for t in range(T):
      evolve( U1, U2, Uout, X, L )
      U1,U2,Uout = Uout,U1,U2
    S = checkSUM( U1, X )
    free(U1)
    free(U2)
    free(Uout)

  print("CheckSum = ", S)


@cython.wraparound(False)
@cython.boundscheck(False)
cdef void evolve( float *U1, float *U2, float *Uout, int X, float L) nogil:
  cdef int x
  cdef float L2 = 2.0*(1.0-L)
  for x in prange(1,X):
    Uout[x] = L2*U1[x] + L*(U1[x+1]+U1[x-1]) - U2[x]

@cython.wraparound(False)
@cython.boundscheck(False)
cdef float checkSUM ( float *In, int X ) nogil:
  cdef float S= 0
  cdef int x
  for x in prange(1,X):
    S += In[x]
  return S

@cython.wraparound(False)
@cython.boundscheck(False)
@cython.cdivision(True)
cdef void init ( float *U1, float *U2, int X, int T ) nogil:
  cdef int x
  U1[0]= 0.0
  U2[0]= 0.0
  U1[X]= 0.0
  U2[X]= 0.0
  for x in prange (1,X):
    U2[x]= sin(x * pi / X)
    U1[x]= U2[x] * cos(pi / (T+1))
