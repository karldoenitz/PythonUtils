# -*- coding: utf-8 -*-

import ctypes
from ctypes import *


lib = ctypes.CDLL("./demo.so")


class Score(Structure):
    _fields_ = [
        ("math", c_float),
        ("national_language", c_float),
        ("english", c_float)
    ]


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


def test_pass_array(list_val):
    size = len(list_val)
    array_obj = c_int * size
    array = array_obj(*list_val)
    sum_array = lib.sum_array
    sum_array.argtypes = [array_obj, c_int]
    sum_array.restype = c_int
    return sum_array(array, size)


def test_pass_float_pointer(list_val):
    size = len(list_val)
    float_pointer_type = POINTER(c_float)
    float_array_type = c_float * size
    float_array = float_array_type(*list_val)
    sum_float_pointer = lib.sum_float_pointer
    sum_float_pointer.argtypes = [float_pointer_type, c_int]
    sum_float_pointer.restype = float_pointer_type
    result = sum_float_pointer(float_array, size)
    return map(float, ["%.2f" % result[index] for index in range(0, size)])


def test_upper_string(input_string):
    size = len(input_string)
    upper_char_array = lib.upper_char_array
    upper_char_array.argtypes = [c_char_p, c_int]
    upper_char_array.restype = c_char_p
    return upper_char_array(c_char_p(input_string), size)


def test_modify_array():
    size = c_int()
    array = pointer(c_int())
    lib.modify_array(
        byref(size),
        byref(array)
    )
    return [array[index] for index in range(0, size.value)]


def test_sum_score(input_score):
    sum_score = lib.sum_score
    sum_score.argtypes = [POINTER(Score)]
    sum_score.restype = c_float
    return sum_score(pointer(input_score))


if __name__ == '__main__':
    print test_int(12, 35)
    print test_float(123.456789, 3.579)
    print test_double(1.23456789, 3.579)
    print test_char("A")
    print test_bool(True)
    print test_pass_array([1, 2, 3, 4, 5])
    print test_pass_float_pointer([1.1, 2.2, 3.3, 4.4, 5.5])
    print test_upper_string("abcdefghijklmnopqrstuvwxyz")
    print test_modify_array()
    # 1
    data = {"math": 100, "national_language": 99, "english": 99.5}
    score = Score(**data)
    print test_sum_score(score)
    # 2
    score = Score()
    score.math = 100
    score.national_language = 99.5
    score.english = 99.5
    print test_sum_score(score)
