# -*- coding: utf-8 -*-

import ctypes
from ctypes import *


lib = ctypes.CDLL("./demo.so")


def test_int(first, second):
    sum_int = lib.sum_int
    sum_int.args_type = [c_int, c_int]
    sum_int.res_type = [c_int]
    return sum_int(first, second)


def test_float(first, second):
    pass


def test_double(first, second):
    pass


def test_char(input):
    pass


def test_bool(input):
    pass


if __name__ == '__main__':
    print test_int(12, 35)
    print test_float(123.456789, 3.579)
    print test_double(1.23456789, 3.579)
    print test_char()
    print test_bool()
