import types
from opcode import HAVE_ARGUMENT, EXTENDED_ARG
from cpython.object cimport PyObject_HasAttr
from py_pal.metric cimport AVG_BUILTIN_FUNCTION_COMPLEXITY, CallMetric

cdef class OpcodeMetric:
    def __init__(self):
        self.hits = 0
        self.builtin_calls = 0

    cdef Py_ssize_t get_value(self, FrameType frame):
        return 1

    cdef bint in_complexity_map(self, function):
        return PyObject_HasAttr(function, '__qualname__') and function.__qualname__ in AVG_BUILTIN_FUNCTION_COMPLEXITY

    cdef Py_ssize_t get_function_opcodes(self, object function, object args, object kwargs):
        cdef CallMetric instance

        if isinstance(function, types.BuiltinFunctionType):
            # Statistics
            self.builtin_calls += 1
            if self.in_complexity_map(function):
                self.hits += 1

        if self.in_complexity_map(function):
            complexity_class = AVG_BUILTIN_FUNCTION_COMPLEXITY[function.__qualname__]
            instance = complexity_class(args, kwargs)
            return instance.value()

        return 1

cdef unpack_oparg(code):
    # Code from dis.py
    cdef int extended_arg = 0
    for i in range(0, len(code), 2):
        op = code[i]
        if op >= HAVE_ARGUMENT:
            arg = code[i + 1] | extended_arg
            extended_arg = (arg << 8) if op == EXTENDED_ARG else 0
        else:
            arg = None
        return arg

cdef class AdvancedOpcodeMetric(OpcodeMetric):
    cdef Py_ssize_t get_value(self, FrameType frame):
        if frame.f_lasti < 0:
            return 1

        code = frame.f_code.co_code
        op = code[frame.f_lasti]

        if op == 131:
            # CALL_FUNCTION
            argc = unpack_oparg(code[frame.f_lasti:])
            valuestack = <list> get_valuestack(<PyFrameObject*> frame, argc + 1)
            args = valuestack[1:]
            _callable = valuestack[0]

            return self.get_function_opcodes(_callable, args, {})

        elif op == 141:
            # CALL_FUNCTION_KW
            argc = unpack_oparg(code[frame.f_lasti:])
            valuestack = <list> get_valuestack(<PyFrameObject*> frame, argc + 2)

            _callable = valuestack.pop(0)
            kw_names = valuestack.pop()
            kwargs = {}
            for name in kw_names:
                kwargs[name] = valuestack.pop()

            return self.get_function_opcodes(_callable, valuestack, kwargs)

        """
        elif op == 142:
            # CALL_FUNCTION_EX
            argc = unpack_oparg(code[frame.f_lasti:])

            if argc:
                valuestack = <list> get_valuestack(<PyFrameObject*> frame, 3)
                length = len(valuestack)
                kwargs = valuestack[length-1]
                args = valuestack[length-2]
                _callable = valuestack[length-3]
            else:
                valuestack = <list> get_valuestack(<PyFrameObject*> frame, 2)
                length = len(valuestack)
                kwargs = {}
                args = valuestack[length-1]
                _callable = valuestack[length-2]

            print(_callable, args, kwargs)
        """

        return 1

"""


elif op == 151:
    # BUILD_MAP_UNPACK_WITH_CALL
    argc = self.get_arg(<_Py_CODEUNIT *> frame.f_code, frame.f_lasti)
    valuestack = <list> self.get_valuestack(<PyFrameObject*> frame, argc + 2)

    #m = valuestack[-argc:]
    #args = {}
    #for _m in m:
    #    args.update(_m)

    # (valuestack[0], args, None)
    print(op, argc, valuestack)

elif op == 158:
    # BUILD_TUPLE_UNPACK_WITH_CALL
    argc = self.get_arg(<_Py_CODEUNIT *> frame.f_code, frame.f_lasti)
    valuestack = <list> self.get_valuestack(<PyFrameObject*> frame, argc + 1)
    #t = valuestack[-argc:]
    #args = tuple(chain(*t))

    # (valuestack[0], args, None)
    print(op, argc, valuestack)

elif op == 161:
    # CALL_METHOD
    argc = self.get_arg(<_Py_CODEUNIT *> frame.f_code, frame.f_lasti)
    valuestack = <list> self.get_valuestack(<PyFrameObject*> frame, argc + 2)
    #method = valuestack[0]
    #instance = valuestack[1]
    #args = ()
    #if argc > 0:
    #    args = valuestack[-1:]
    #if not method:
    #    method = instance

    #(method, args, None)
    print(op, argc, valuestack)
"""


"""
op = frame.f_code.co_code[frame.f_lasti]
last_op = opname[op]

if op == 81:
    # WITH_CLEANUP_START
    pass

elif op == 143:
    # SETUP_WITH
    pass

elif op == 93:
    # FOR_ITER
    pass

elif op == 86:
    # YIELD_VALUE
    pass

elif op == 83:
    # RETURN_VALUE
    pass

elif op == 68:
    # GET_ITER
    valuestack = <list> get_valuestack(<PyFrameObject*> frame, 1)

    # Make a copy because generators cannot be copied, may be needed in CALL_FUNCTION_EX
    if not isinstance(valuestack[-1], GeneratorType):
        self.last_gen = iter(valuestack[-1])

elif op == 131:
    # CALL_FUNCTION

    # TODO: Look into cpython's 'ceval.c' and use already implemented
    #  functionality to determine arguments for opcode weight calculation

    argc = get_argval(frame.f_code, frame.f_lasti)
    valuestack = <list> get_valuestack(<PyFrameObject*> frame, argc + 1)
    f_last = (valuestack[0], valuestack[1:], None)

    # (valuestack[0], valuestack[1:], None)

elif op == 141:
    # CALL_FUNCTION_KW
    argc = get_argval(frame.f_code, frame.f_lasti)
    valuestack = <list> get_valuestack(<PyFrameObject*> frame, argc + 2)

    kw = valuestack[-1]
    args = valuestack[-(argc + 1):-1]
    kwargs = {k: v for k, v in zip(kw, args[::-1])}
    args = args[:-len(kw)]

    # (valuestack[0], args, kwargs)

elif op == 142:
    # CALL_FUNCTION_EX
    argc = get_argval(frame.f_code, frame.f_lasti)

    if argc:
        valuestack = <list> get_valuestack(<PyFrameObject*> frame, 3)
        kwargs = valuestack[-1]
        args = valuestack[-2]
        function = valuestack[-3]
    else:
        valuestack = <list> get_valuestack(<PyFrameObject*> frame, 2)
        kwargs = {}
        args = valuestack[-1]
        function = valuestack[-2]

    f_last = (
        function,
        args if not isinstance(args, GeneratorType) else self.last_gen,
        kwargs
    )

    #(
    #    function,
    #    args if not isinstance(args, GeneratorType) else self.last_gen,
    #    kwargs
    #)

elif op == 151:
    # BUILD_MAP_UNPACK_WITH_CALL
    argc = get_argval(frame.f_code, frame.f_lasti)
    valuestack = <list> get_valuestack(<PyFrameObject*> frame, argc + 2)

    m = valuestack[-argc:]
    args = {}
    for _m in m:
        args.update(_m)

    # (valuestack[0], args, None)

elif op == 158:
    # BUILD_TUPLE_UNPACK_WITH_CALL
    argc = get_argval(frame.f_code, frame.f_lasti)
    valuestack = <list> get_valuestack(<PyFrameObject*> frame, argc + 1)
    t = valuestack[-argc:]
    args = tuple(chain(*t))

    # (valuestack[0], args, None)

elif op == 161:
    # CALL_METHOD
    argc = get_argval(frame.f_code, frame.f_lasti)
    valuestack = <list> get_valuestack(<PyFrameObject*> frame, argc + 2)
    method = valuestack[0]
    instance = valuestack[1]
    args = ()
    if argc > 0:
        args = valuestack[-1:]
    if not method:
        method = instance

    #(method, args, None)
"""
