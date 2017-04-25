# -*-encoding:utf-8-*-
"""

engine
~~~~~~

introduction
this module supply database engine.

Usage
=====
>>> from model import Model
>>> engine = Engine(EngineName.sqLite, sqlite="test.sqlite").create()
>>> class User(Model):
...    class Meta:
...        engine = engine
...        table_name = "user"
>>>

"""
from database_manager.mysql_dbm.database_manager import DatabaseManager as MySqlDBM
from database_manager.sqlite_dbm.database_manager import DataBaseManager as SqLiteDBM

__author__ = "karlvorndoenitz@gmail.com"


class EngineName(object):
    MySQL = "mysql"
    sqLite = "sqLite"


class Engine(object):
    def __init__(self, engine_name, **kwargs):
        """
        
        :param engine_name: engine's name, must use EngineName's value
        :param kwargs: the attributes about engine
        
        """
        if engine_name == EngineName.MySQL:
            self.dbm = MySqlDBM(
                host=kwargs["host"],
                port=kwargs["port"],
                user=kwargs["user"],
                pwd=kwargs["pwd"],
                db=kwargs["db"]
            )
        elif engine_name == EngineName.sqLite:
            self.dbm = SqLiteDBM(kwargs["sqlite"])

    def create(self):
        """ get database's database Manager
        
        :return: database manager
        
        """
        return self.dbm
