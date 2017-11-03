//
// Created by karl on 17-11-1.
//

#include <Python.h>

static PyObject *wrap_pass_parameters(PyObject *self, PyObject *args) {
    double sum = 0;
    char *input_string;
    PyDictObject *input_dict;
    PyListObject *input_list;
    float input_float;
    if (!PyArg_ParseTuple(args, "OOfs", &input_dict, &input_list, &input_float, &input_string)) {
        return NULL;
    }
    int i, j;
    for (i = 0; i < PyList_Size((PyObject *)input_list); ++i) {
        sum += PyFloat_AsDouble(PyList_GetItem((PyObject *)input_list, i));
    }
    PyObject *dict_keys = PyDict_Keys((PyObject *)input_dict);
    for (j = 0; j < PyDict_Size((PyObject *)input_dict); ++j) {
        PyObject *key = PyList_GetItem(dict_keys, j);
        PyObject *value = PyDict_GetItem((PyObject *)input_dict, key);
        sum += PyFloat_AsDouble(value);
    }
    sum += input_float;
    PyObject *result = PyDict_New();
    PyObject *sum_num = Py_BuildValue("f", sum);
    PyDict_SetItemString(result, input_string, sum_num);
    return result;
}

static PyObject *wrap_pass_obj(PyObject *self, PyObject *args) {
    PyObject *instance_object;
    if (!PyArg_ParseTuple(args, "O", &instance_object)) {
        return NULL;
    }
    PyObject *first_attribute = PyObject_GetAttrString(instance_object, "first");
    PyObject *second_attribute = PyObject_GetAttrString(instance_object, "second");
    double first_num = PyFloat_AsDouble(first_attribute);
    double second_num = PyFloat_AsDouble(second_attribute);
    double sum = first_num + second_num;
    PyObject *result = Py_BuildValue("f", sum);
    return result;
}

/* registration table  */
static PyMethodDef wrap_methods[] ={
        {"pass_parameters", wrap_pass_parameters, METH_VARARGS},       /* method name, C func ptr, always-tuple */
        {"pass_obj", wrap_pass_obj, METH_VARARGS},       /* method name, C func ptr, always-tuple */
        {NULL, NULL}                   /* end of table marker */
};

/* module initializer 注意此处，init后面必须与文件名相同！！！*/
PyMODINIT_FUNC initdemo(void)                       /* called on first import */
{                                      /* name matters if loaded dynamically */
    (void)Py_InitModule("demo", wrap_methods);   /* mod name, table ptr */
}
