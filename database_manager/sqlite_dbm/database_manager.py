# -*-encoding:utf-8-*-
"""

database_manager
~~~~~~~~~~~~~~~~~~

introduction
use this module to operate sqlite database,
execute sql or save data to database.

Usage
=====
>>> from database_manager.sqlite_dbm.database_manager import DataBaseManager
>>> db_manager = DataBaseManager()
>>> db_manager.execute("SELECT id, name FROM user_info WHERE id = 3")
[{'id': 3, 'name': 'Alice'}]
>>> db_manager.save(
...     "user_info",
...     {
...         "id": 6,
...         "name": "Ada"
...     }
... )
6

"""
import json
import logging
import sqlite3

from ..utils import *


class DataBaseManager(object):
    def __init__(self):
        self.logger = logging.getLogger()
        self.connection = sqlite3.connect(":memory:")
        self.connection.row_factory = self.__dict_factory
        self.cursor = self.connection.cursor()

    @classmethod
    def __dict_factory(cls, cursor, row):
        """ convert sqlite3 select result to dict

        :param cursor: sqlite3's cursor
        :param row: select result
        :return: a dict contains the data of a record

        """
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def execute(self, sql):
        """ execute sql

        :param sql: sql will be executed
        :return: execute result

        """
        results = self.cursor.execute(sql)
        results = results.fetchall()
        return results

    def query_obj(self, sql, model_name="QueryResultObject"):
        """ execute sql
        
        :param sql: sql will be executed
        :param model_name: model's name, default QueryResultObject
        :return: execute result, contains objects
        
        """
        result = [dict_to_object(model_name, data) for data in self.execute(sql)]
        return result

    def save(self, table_name, record_dict, is_insert_id=False):
        """

        :param table_name: table's name
        :param record_dict: a dict contains data
        :return: the last record id, if save failed return 0

        """
        self.logger.info(json.dumps(record_dict, ensure_ascii=False))
        sql_template = "INSERT INTO %s (%s) VALUES (%s)"
        column_name_list = record_dict.keys()
        column_names = ",".join(column_name_list)
        value_list = []
        for column_name in column_name_list:
            value = record_dict.get(column_name)
            if isinstance(value, str):
                value = "'%s'" % value
            elif isinstance(value, unicode):
                value = value.encode("utf-8")
                value = "'%s'" % value
            elif value is None:
                value = "NULL"
            else:
                value = str(value)
            value_list.append(value)
        column_values = ",".join(value_list)
        sql = sql_template % (table_name, column_names, column_values)
        self.logger.info(sql)
        try:
            self.cursor.execute(sql)
            self.cursor.execute(sql)
            self.connection.commit()
            if not is_insert_id:
                return
            return self.cursor.lastrowid
        except Exception, e:
            self.logger.error(e)
            return 0
