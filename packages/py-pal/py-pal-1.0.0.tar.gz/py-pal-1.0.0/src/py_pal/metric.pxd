cdef class CallMetric:
    cdef object args
    cdef object kwargs
    cdef Py_ssize_t value(self)

cdef class ArgsLengthLinear(CallMetric):
    pass

cdef public dict AVG_BUILTIN_FUNCTION_COMPLEXITY