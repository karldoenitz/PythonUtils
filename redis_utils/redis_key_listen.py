# -*- coding: utf-8 -*-
"""

redis_key_listen
~~~~~~~~~~~~~~~~

introduction
this module listen key space whether modified in redis.

input this command into console
$ redis-cli config set notify-keyspace-events KEA

Usage
=====
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
...     print time.time(), msg.msg
...
>>> redis_key_event_listen(redis_instance, print_msg)
1401548400.27 {'pattern': None, 'type': 'psubscribe', 'channel': '*', 'data': 1L}

"""


class RedisKeyListener(object):
    _msg_fields = ["pattern", "type", "channel", "data"]
    _obj_fields = ["msg", "key", "operate", "db"]

    def __init__(self, msg):
        msg_dict = dict(msg)
        setattr(self, "msg", msg)
        for k in self._obj_fields[1:]:
            setattr(self, k, "")
        for msg_k in self._msg_fields:
            setattr(self, msg_k, msg_dict.get(msg_k))
        if self.channel.startswith("__keyspace"):
            setattr(self, "key", ":".join(self.channel.split(":")[1:]))
            setattr(self, "operate", self.data)
            setattr(self, "db", self.channel.split("@")[1].split("__")[0])
        elif self.channel.startswith("__keyevent"):
            setattr(self, "key", self.data)
            setattr(self, "operate", ":".join(self.channel.split(":")[1:]))
            setattr(self, "db", self.channel.split("@")[1].split("__")[0])

    def __getattr__(self, name):
        if name not in self._msg_fields + self._obj_fields:
            raise AttributeError('%s object has no attribute: %s' % (self.__class__.__name__, name))
        value = self.data.get(name)
        return value


def redis_key_event_listen(r, call_back, scribe="*"):
    """ use call back function to listen key event space

    :param r: redis instance
    :param call_back: call back function
    :param scribe: scribe characters default *
    :return:

    """
    try:
        pub_sub = r.pubsub()
        pub_sub.psubscribe(scribe)
        for msg in pub_sub.listen():
            call_back(RedisKeyListener(msg))
    except Exception as e:
        print(e)
