# -*-encoding:utf-8-*-
"""

async
~~~~~~~~~~~~~~~~~~

introduction
use this module to run a function async,
start a new thread to run the function.

Usage
=====
>>> from thread_utils.async import async
>>> @async
... def func_sum(first, second):
...     print first + second
>>> func_sum(1, 2)

"""
import threading
import functools


def async(func):
    """ async methods
    :param func: function's reference
    :return: wrapper
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        new_thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        new_thread.start()
    return wrapper
