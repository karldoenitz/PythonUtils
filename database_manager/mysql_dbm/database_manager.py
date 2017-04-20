# -*-encoding:utf-8-*-
"""

database_manager
~~~~~~~~~~~~~~~~~~

introduction
use this module to operate MySQL database,
execute sql or save data to database.

Usage
=====
>>> from database_manager.mysql_dbm.database_manager import DatabaseManager
>>> db_manager = DatabaseManager()
>>> db_manager.query("SELECT id, name FROM user_info WHERE id = 3")
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
import MySQLdb
import MySQLdb.cursors

from ..utils import *


class DatabaseManager(object):
    def __init__(self):
        self.logger = logging.getLogger()
        self.connection = MySQLdb.connect(
            host="",
            port="",
            user="",
            passwd="",
            db="",
            charset="utf8",
            cursorclass=MySQLdb.cursors.DictCursor
        )
        self.cursor = self.connection.cursor()

    def query(self, sql):
        """ execute a sql query

        :param sql: sql query
        :return: query result

        """
        try:
            self.logger.info(sql)
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data
        except Exception, e:
            self.logger.error(e)
            return {}

    def query_obj(self, sql):
        """ execute a sql query and return an object
        
        :param sql: sql query
        :return: query result
        
        """
        try:
            self.logger.info(sql)
            self.cursor.execute(sql)
            result = [dict_to_object("QueryResultObject", data) for data in self.cursor.fetchall()]
            return result
        except Exception, e:
            self.logger.error(e)
            return {}

    def execute(self, sql):
        """ execute sql

        :param sql: sql will be executed
        :return: execute result, True or False

        """
        try:
            self.logger.info(sql)
            self.cursor.execute(sql)
            self.connection.commit()
            return True
        except Exception, e:
            self.logger.error(e)
            return False

    def close(self):
        self.cursor.close()
        self.connection.close()

    def save(self, table_name, record_dict, is_insert_id=False):
        """ save a dict to database

        :param table_name: table's name
        :param record_dict: a dict contains the data of a record
        :param is_insert_id: whether need return last record id
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
            if is_insert_id:
                self.cursor.execute(sql)
                success_column = int(self.connection.insert_id())
            else:
                success_column = self.cursor.execute(sql)
            self.connection.commit()
            return success_column
        except Exception, e:
            self.logger.error(e)
            return 0
