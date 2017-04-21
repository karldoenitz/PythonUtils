# -*- coding: utf-8 -*-
"""

utils
~~~~~~

introduction
this module contains some utils such as dict_to_object etc.

Usage
=====
>>> user_dict = {
...     "name": "Ada Wong",
...     "age": 18,
...     "gender": "female"
... }
>>> user_obj = dict_to_object("User", user_dict)
>>> print type(user_obj)
User
>>> print user_obj.name
Ada Wong
>>> class User(object):
...     name = "Ada Wong"
...     age = 18
...     gender = "female"
...
>>> user = User()
>>> user.age = 16
>>> print object_to_dict(user)
{'name': 'Ada Wong', 'age': 16, 'gender': 'female'}

"""

import types

__author__ = "karlvorndoenitz@gmail.com"


def dict_to_object(class_name, dictionary):
    """ convert a dictionary to an object
    
    :param class_name: the name of object's type
    :param dictionary: the dictionary will be converted
    :return: an object
    
    """
    return type(class_name, (object,), dictionary)()


def object_to_dict(obj):
    """ convert an object to a dictionary
    
    :param obj: the object will be converted to a dictionary
    :return: the dictionary converted from an object
    
    """
    dictionary = dict(
        (name, getattr(obj, name)) for name in dir(obj)
        if not name.startswith('__')
        and not isinstance(getattr(obj, name), types.FunctionType)
        and not isinstance(getattr(obj, name), types.MethodType)
        and not isinstance(getattr(obj, name), types.ClassType)
    )
    return dictionary


def add_slashes(s):
    """ add slashes to a string
    
    :param s: the string will be slashed
    :return: the string add slashes
    
    """
    d = {'"': '\\"', "'": "\\'"}
    s = s.decode()
    return ''.join(d.get(c, c) for c in s)
