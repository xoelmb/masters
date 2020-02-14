import cython
from libc.math cimport sin

cpdef float eval_fitness( float x, float y ):
    return x * sin(4 * x) + 1.1 * y * sin(2 * y)