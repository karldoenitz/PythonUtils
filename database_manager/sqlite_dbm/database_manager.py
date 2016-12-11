# -*-encoding:utf-8-*-
import sqlite3
import logging
import json


class DataBaseManager(object):
    def __init__(self):
        self.logger = logging.getLogger()
        self.connection = sqlite3.connect(":memory:")
        self.connection.row_factory = self.__dict_factory
        self.cursor = self.connection.cursor()

    @classmethod
    def __dict_factory(cls, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def execute(self, sql):
        results = self.cursor.execute(sql)
        results = results.fetchall()
        return results

    def save(self, table_name, record_dict):
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
            return self.cursor.lastrowid
        except Exception, e:
            self.logger.error(e)
            return 0
