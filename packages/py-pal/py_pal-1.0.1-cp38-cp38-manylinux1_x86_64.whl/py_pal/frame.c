#include "Python.h"
#include "frameobject.h"
#include "frame.h"

#include "code.h"
#include "opcode.h"

static PyObject* get_valuestack(PyFrameObject* f, Py_ssize_t index) {
    PyObject* lst = PyList_New(0);
    if (f->f_stacktop != NULL) {
        PyObject** p = f->f_stacktop;
        p--;
        for (p; p >= f->f_valuestack; p--) {
            if (--index < 0) break;
            if (*p != NULL)
                PyList_Append(lst, *p);
            else
                PyList_Append(lst, Py_None);
        }
    }

    PyList_Reverse(lst);
    return lst;
}


static PyObject* get_valuestack_full(PyFrameObject* f) {
    PyObject* lst = PyList_New(0);
    if (f->f_stacktop != NULL) {
        PyObject** p = NULL;
        for (p = f->f_valuestack; p < f->f_stacktop; p++) {
            if (*p != NULL)
                PyList_Append(lst, *p);
            else
                PyList_Append(lst, Py_None);
        }
    }

    return lst;
}


/* Code from cpython's frameobject.c */


/* Given the index of the effective opcode,
   scan back to construct the oparg with EXTENDED_ARG */
static unsigned int get_arg(const _Py_CODEUNIT *codestr, Py_ssize_t i)
{
    _Py_CODEUNIT word;
    unsigned int oparg = _Py_OPARG(codestr[i]);
    if (i >= 1 && _Py_OPCODE(word = codestr[i-1]) == EXTENDED_ARG) {
        oparg |= _Py_OPARG(word) << 8;
        if (i >= 2 && _Py_OPCODE(word = codestr[i-2]) == EXTENDED_ARG) {
            oparg |= _Py_OPARG(word) << 16;
            if (i >= 3 && _Py_OPCODE(word = codestr[i-3]) == EXTENDED_ARG) {
                oparg |= _Py_OPARG(word) << 24;
            }
        }
    }
    return oparg;
}