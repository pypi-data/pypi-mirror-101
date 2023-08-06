from cpython.object cimport PyObject

cdef extern from "frameobject.h":
    ctypedef struct PyFrameObject
    ctypedef struct _Py_CODEUNIT

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

cdef extern from "frame.c":
    PyObject *get_valuestack_full(PyFrameObject *frame)
    PyObject *get_valuestack(PyFrameObject*frame, Py_ssize_t index)
    unsigned int get_arg(_Py_CODEUNIT *codestr, Py_ssize_t i)

cdef class OpcodeMetric:
    cdef readonly Py_ssize_t hits
    cdef readonly Py_ssize_t builtin_calls
    cdef Py_ssize_t get_value(self, FrameType frame)
    cdef Py_ssize_t get_function_opcodes(self, object function, object args, object kwargs)
    cdef bint in_complexity_map(self, object function)

cdef class AdvancedOpcodeMetric(OpcodeMetric):
    pass
