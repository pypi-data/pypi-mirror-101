#ifndef FRAME_H
#define FRAME_H

static PyObject* get_valuestack_full(PyFrameObject* f);
static PyObject* get_valuestack(PyFrameObject* f, Py_ssize_t index);
static unsigned int get_arg(const _Py_CODEUNIT *codestr, Py_ssize_t i);

#endif