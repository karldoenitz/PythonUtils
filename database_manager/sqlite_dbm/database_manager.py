# -*-encoding:utf-8-*-
import sqlite3


class DataBaseManager(object):
    def __init__(self):
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
