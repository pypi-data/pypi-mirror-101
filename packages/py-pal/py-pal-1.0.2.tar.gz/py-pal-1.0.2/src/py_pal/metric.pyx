from math import log, ceil

from cpython.genobject cimport PyGen_Check
from cpython.object cimport PyObject_HasAttr

cdef class CallMetric:
    """
        Average case complexities

        Generally, 'n' is the number of elements currently in the container.
        'k' is either the value of a parameter or the number of elements in the parameter.

        As in:  https://wiki.python.org/moin/TimeComplexity
    """

    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs

    cdef Py_ssize_t value(self):
        raise NotImplementedError("Must be implemented by subclass.")

cdef class ArgsLengthLinear(CallMetric):
    cdef Py_ssize_t value(self):
        if all(map(lambda x: PyObject_HasAttr(x, '__iter__'), self.args)):
            return sum(map(lambda x: len([x]) if PyGen_Check(x) else len(x), self.args))
        return len(self.args)

cdef class FirstArgLengthLogarithmic(CallMetric):
    """Expects a collection as first argument."""
    cdef Py_ssize_t value(self):
        return ceil(log(len(self.args[0]), 2))

cdef class ArgsLinear(CallMetric):
    cdef Py_ssize_t value(self):
        return self.args[0]

"""
Map of Python builtin functions to average case time-complexity.
All complexity classes are based on the CPython implementation.
"""

# Unlisted functions are implicitly defined as constant
AVG_BUILTIN_FUNCTION_COMPLEXITY = {
    #Random.getrandbits.__qualname__: ArgsLinear,
    #abs.__qualname__: Constant,
    #all.__qualname__: Constant,
    #any.__qualname__: Constant,
    #ascii.__qualname__: Constant,
    #bin.__qualname__: Constant,
    #chr.__qualname__: Constant,
    #delattr.__qualname__: Constant,
    #divmod.__qualname__: Constant,
    #format.__qualname__: Constant,
    #getattr.__qualname__: Constant,
    #hasattr.__qualname__: Constant,
    #hash.__qualname__: Constant,
    #hex.__qualname__: Constant,
    #id.__qualname__: Constant,
    #iter.__qualname__: Constant,
    #len.__qualname__: Constant,
    max.__qualname__: ArgsLengthLinear,
    min.__qualname__: ArgsLengthLinear,
    #oct.__qualname__: Constant,
    #ord.__qualname__: Constant,
    #pow.__qualname__: Constant,
    #print.__qualname__: Constant,
    #repr.__qualname__: Constant,
    #round.__qualname__: Constant,
    #setattr.__qualname__: Constant,
    sorted.__qualname__: FirstArgLengthLogarithmic,
    #sum.__qualname__: Constant,
    #range.__qualname__: Range,
    #reversed.__qualname__: FirstArgLengthLinear,
}
