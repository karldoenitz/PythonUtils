# -*- coding: utf-8 -*-

import ctypes
from ctypes import *


lib = ctypes.CDLL("./demo.so")


def test_int(first, second):
    sum_int = lib.sum_int
    sum_int.argtypes = [c_int, c_int]
    sum_int.restype = c_int
    return sum_int(first, second)


def test_float(first, second):
    sum_float = lib.sum_float
    sum_float.argtypes = [c_float, c_float]
    sum_float.restype = c_float
    return sum_float(c_float(first), c_float(second))


def test_double(first, second):
    sum_double = lib.sum_double
    sum_double.argtypes = [c_double, c_double]
    sum_double.restype = c_double
    return sum_double(first, second)


def test_char(input_val):
    modify_char = lib.modify_char
    modify_char.argtypes = [c_char]
    modify_char.restype = c_char
    return modify_char(input_val)


def test_bool(input_val):
    modify_bool = lib.modify_bool
    modify_bool.argtypes = [c_bool]
    modify_bool.restype = c_bool
    return modify_bool(input_val)


if __name__ == '__main__':
    print test_int(12, 35)
    print test_float(123.456789, 3.579)
    print test_double(1.23456789, 3.579)
    print test_char("A")
    print test_bool(True)
