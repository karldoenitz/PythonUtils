# -*- coding: utf-8 -*-
"""

redis_key_listen
~~~~~~~~~~~~~~~~

introduction
this module listen key space whether modified in redis.

Usage
=====
input this command into console
$ redis-cli config set notify-keyspace-events KEA
>>> import redis
>>> import time
>>> redis_settings = {
...     "host": "localhost",
...     "port": 6379,
...     "db": 0
... }
...
>>> redis_instance = redis.StrictRedis(**redis_settings)
>>> def print_msg(msg):
...     print time.time(), msg
...
>>> redis_key_event_listen(redis_instance, print_msg)
1401548400.27 {'pattern': None, 'type': 'psubscribe', 'channel': '*', 'data': 1L}

"""


def redis_key_event_listen(r, call_back):
    """ use call back function to listen key event space

    :param r: redis instance
    :param call_back: call back function
    :return:

    """
    try:
        pub_sub = r.pubsub()
        pub_sub.psubscribe("*")
        for msg in pub_sub.listen():
            call_back(msg)
    except Exception as e:
        print(e)
