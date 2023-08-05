import cython
from cpython.pystate cimport Py_tracefunc

from py_pal.opcode_metric cimport OpcodeMetric

cdef extern from "frameobject.h":
    ctypedef struct PyObject

    ctypedef class types.CodeType[object PyCodeObject]:
        cdef object co_filename
        cdef int co_firstlineno
        cdef object co_code
        cdef str co_name
        cdef int co_argcount
        cdef tuple co_varnames

    ctypedef class types.FrameType[object PyFrameObject]:
        cdef CodeType f_code
        cdef PyObject *f_trace
        cdef object f_globals
        cdef object f_locals
        cdef int f_lineno
        cdef char f_trace_lines
        cdef char f_trace_opcodes
        cdef int f_lasti
        cdef PyObject *f_valuestack
        cdef PyObject *f_stacktop
        #cdef PyObject *f_localsplus[1]

    void PyEval_SetTrace(Py_tracefunc func, PyObject *obj)
    void PyEval_SetProfile(Py_tracefunc func, PyObject *obj)
    void PyFrame_FastToLocals(FrameType frame)

@cython.final
cdef class Tracer:
    cdef:
        Py_ssize_t call_id
        dict opcodes
        list calls
        dict f_weight_map
        readonly dict f_map
        list call_stack
        list blacklist
        list functions
        OpcodeMetric metric

    cpdef object get_call_stats(self)
    cpdef object get_opcode_stats(self)
