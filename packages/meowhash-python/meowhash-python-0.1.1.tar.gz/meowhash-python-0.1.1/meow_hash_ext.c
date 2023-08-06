#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdbool.h>
#include "meow_hash_x64_aesni.h"


PyObject * meth_digest(PyObject * self, PyObject * args, PyObject * kwargs)
{
    static char * keywords[] = {"byte_buffer", NULL};
    PyObject * byte_buffer;

    int succeed = PyArg_ParseTupleAndKeywords(
        args,
        kwargs,
        "S",
        keywords,
        &byte_buffer
    );

    if (!succeed)
        return 0;  // Python will set error message for us

    int size = PyBytes_Size(byte_buffer);
    char * buffer = PyBytes_AsString(byte_buffer);

    if (!buffer)
        return 0;  // Python will set error message for us

    meow_u128 hash = MeowHash(MeowDefaultSeed, size, buffer);

    return Py_BuildValue("y#", (char *)&hash, 16);
}


PyMethodDef module_methods[] = {
    {"digest", (PyCFunction)meth_digest, METH_VARARGS | METH_KEYWORDS, 0},
    {0}
};


PyModuleDef module_def = {
    PyModuleDef_HEAD_INIT, "meow_hash_ext", 0, -1, module_methods, 0, 0, 0, 0
};


PyObject * PyInit_meow_hash_ext()
{
    PyObject * module = PyModule_Create(&module_def);
    return module;
}
