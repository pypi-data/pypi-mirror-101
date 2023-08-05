from collections import deque

import numpy as np
from py_pal.opcode_metric cimport AdvancedOpcodeMetric, OpcodeMetric

cdef tuple WHAT_NAMES = ("call", "exception", "line", "return", "c_call", "c_exception", "c_return", "opcode")

cdef class Tracer:
    def __init__(self, OpcodeMetric metric=AdvancedOpcodeMetric()):
        self.blacklist = [
            "py_pal.tracer",
            "importlib._bootstrap",
            "importlib._bootstrap_external"
        ]
        self.metric = metric
        self.call_id = 0
        self.calls = [(self.call_id, 0, '__main__', 0, '<module>', None, None, None, None, None, None, None, None)]
        self.opcodes = {}
        self.f_weight_map = {}
        self.call_stack = [(self.call_id, 0)]
        self.call_id += 1

    def __call__(self, frame, what, arg):
        if frame.f_globals.get('__name__', '') not in self.blacklist:
            # Do not measure inside of tracing machinery
            PyEval_SetTrace(<Py_tracefunc> trace_func, <PyObject *> self)

        return self

    def trace(self):
        PyEval_SetTrace(<Py_tracefunc> trace_func, <PyObject *> self)
        return self

    def stop(self):
        PyEval_SetTrace(NULL, NULL)

    cpdef get_call_stats(self):
        return np.asarray(self.calls)

    cpdef get_opcode_stats(self):
        return np.asarray([(*k, v) for k, v in self.opcodes.items()])

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

cdef int last_lineno

cdef int trace_func(Tracer self, FrameType frame, int what, PyObject *arg) except -1:
    """
    The events are emitted after opcode execution.
    Use the call and return events to structure the calls into a hierarchy.
    """
    frame.f_trace_opcodes = 1
    frame.f_trace_lines = 0

    global last_lineno

    #if frame.f_globals.get('__name__', '') in self.blacklist:
    #    return 0

    # if what == 1:
    #    print(<str> arg)
    # self.stop()

    if what == 0:
        # event: call

        # Add call as row (module, function, args, kwargs)
        self.call_stack.append((self.call_id, last_lineno))

        PyFrame_FastToLocals(frame)
        _args, kwonlyargs, _varargs, _varkw = _getfullargs(frame.f_code)

        if isinstance(_args, list):
            _args = tuple(_args)

        if isinstance(kwonlyargs, list):
            kwonlyargs = tuple(kwonlyargs)

        if isinstance(_varargs, list):
            _varargs = tuple(_varargs)

        if isinstance(_varkw, list):
            _varkw = tuple(_varkw)

        args = tuple(map(lambda x: frame.f_locals[x], _args)) if _args else ()
        kwargs = tuple(map(lambda x: frame.f_locals[x], kwonlyargs)) if kwonlyargs else ()
        varargs = frame.f_locals[_varargs] if _varargs else ()
        varkw = frame.f_locals[_varkw].values() if _varkw else ()

        self.calls.append((
            self.call_id,
            id(frame.f_code),
            frame.f_code.co_filename,
            frame.f_lineno,
            frame.f_code.co_name,
            _args,
            tuple(map(lambda x: get_input_factor(x), args)) if args else None,
            kwonlyargs,
            tuple(map(lambda x: get_input_factor(x), kwargs)) if kwargs else None,
            _varargs,
            tuple(map(lambda x: get_input_factor(x), varargs)) if varargs else None,
            _varkw,
            tuple(map(lambda x: get_input_factor(x), varkw)) if varkw else None
        ))
        self.call_id += 1

    elif what == 3:
        # event: return
        if len(self.call_stack) > 1:
            # Do not pop root call row
            child = self.call_stack.pop()
        else:
            child = self.call_stack[0]

        # Add opcode weight to parent call
        parent = self.call_stack[len(self.call_stack) - 1]
        value = self.f_weight_map.get(child[0], 0)
        parent_weight = self.opcodes.get(parent, 0)
        self.opcodes[parent] = parent_weight + value

        _value = self.f_weight_map.get(parent[0], 0)
        self.f_weight_map[parent[0]] = _value + value

    elif what == 7:
        # event: opcode
        # Anything in here should cause minimal overhead
        last_lineno = frame.f_lineno
        metric_value = self.metric.get_value(frame)

        # Save opcode weight per line in current call
        call = self.call_stack[len(self.call_stack) - 1][0]
        key = (call, frame.f_lineno)
        value_line = self.opcodes.get(key, 0)
        self.opcodes[key] = value_line + metric_value

        # Keep track of all opcodes executed within call
        value = self.f_weight_map.get(call, 0)
        self.f_weight_map[call] = value + metric_value

    return 0

cdef Py_ssize_t get_input_factor(arg):
    """
    Proxy for input arguments. Is used to infer complexity with the least squares algorithm.
    Therefore all returned values have to be positive and greater than zero.
    """
    if arg is None or NULL or isinstance(arg, bool):
        return 1

    elif isinstance(arg, np.ndarray):
        return sum(arg.shape)

    elif isinstance(arg, np.generic):
        value = abs(int(arg))
        return value if value > 0 else 1

    elif isinstance(arg, int):
        # The memory size of an ``int`` object is constant.
        # Return ``int`` value to be able to derive simple algorithms.
        if arg == 0:
            return 1
        return abs(arg)

    elif isinstance(arg, (list, dict, set, deque, str, tuple)):
        # Length of collections
        l = len(arg)
        return l if l > 0 else 1

    else:
        return sizeof(arg)

cdef _getfullargs(co):
    nargs = co.co_argcount
    names = co.co_varnames
    nkwargs = co.co_kwonlyargcount
    args = list(names[:nargs])
    kwonlyargs = list(names[nargs:nargs + nkwargs])

    nargs += nkwargs
    varargs = None
    if co.co_flags & 4:
        varargs = co.co_varnames[nargs]
        nargs = nargs + 1
    varkw = None
    if co.co_flags & 8:
        varkw = co.co_varnames[nargs]
    return args, kwonlyargs, varargs, varkw
