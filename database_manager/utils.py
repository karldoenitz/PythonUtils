# -*- coding: utf-8 -*-

__author__ = "karlvorndoenitz@gmail.com"


def dict_to_object(class_name, dictionary):
    """ convert a dictionary to an object
    
    :param class_name: the name of object's type
    :param dictionary: the dictionary will be converted
    :return: an object
    
    """
    return type(class_name, (object,), dictionary)()
