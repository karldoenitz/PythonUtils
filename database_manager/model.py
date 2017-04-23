# -*-encoding:utf-8-*-

from mysql_dbm.database_manager import DatabaseManager
from utils import obj_field_to_dict

__author__ = "karlvorndoenitz@gmail.com"


class Model(object):

    def save(self):
        table_name = self.Meta.table_name
        attr_dict = obj_field_to_dict(self)
        return DatabaseManager.save(table_name, attr_dict, True)

    def get(self, **kwargs):
        pass

    def filter(self, **kwargs):
        pass

    class Meta:
        pass
