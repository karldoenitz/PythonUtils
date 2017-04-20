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

"""

__author__ = "karlvorndoenitz@gmail.com"


def dict_to_object(class_name, dictionary):
    """ convert a dictionary to an object
    
    :param class_name: the name of object's type
    :param dictionary: the dictionary will be converted
    :return: an object
    
    """
    return type(class_name, (object,), dictionary)()
