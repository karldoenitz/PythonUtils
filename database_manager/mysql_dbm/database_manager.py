# -*-encoding:utf-8-*-

import MySQLdb
import MySQLdb.cursors
import logging
import json


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
        try:
            self.logger.info(sql)
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data
        except Exception, e:
            self.logger.error(e)
            return {}

    def execute(self, sql):
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
