# -*- coding: utf-8 -*-

from c_embedding.demo import pass_parameters, pass_obj


class Test(object):
    def __init__(self):
        self.first = 1
        self.second = 2


class T(object):
    first = 100
    second = 200


t = Test()
print pass_obj(t)
print pass_obj(T)
print pass_parameters({"a": 1.1, 2: 2}, [3.3, 4, 5.5], 0.23, "result")
