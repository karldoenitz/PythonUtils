#include <Python.h>

static PyObject *wrap_pass_parameters(PyObject *self, PyObject *args) {
    char *input_str;
    if (!PyArg_ParseTuple(args, "s", &input_str)) {
        return NULL;
    }
    PyObject *pyObject = Py_BuildValue("s", result);
    PyMem_Free(result);
    return pyObject;
}

/* registration table  */
static PyMethodDef wrap_methods[] ={
        {"pass_parameters", wrap_pass_parameters, METH_VARARGS},       /* method name, C func ptr, always-tuple */
        {NULL, NULL}                   /* end of table marker */
};

/* module initializer */
PyMODINIT_FUNC initencryption(void)                       /* called on first import */
{                                      /* name matters if loaded dynamically */
    (void)Py_InitModule("demo", wrap_methods);   /* mod name, table ptr */
}