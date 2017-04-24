# -*-encoding:utf-8-*-
"""

"""

from utils import object_to_dict

__author__ = "karlvorndoenitz@gmail.com"


class Model(object):

    def save(self):
        """ save model to db
        
        :return: True or False
        
        """
        table_name = self.Meta.table_name
        attr_dict = object_to_dict(self)
        return self.Meta.engine.save(table_name, attr_dict, True)

    def get(self, **kwargs):
        """ get a record from db
        
        :param kwargs: condition
        :return: result or Exception
        
        """
        result = self.filter(**kwargs)
        if len(result) == 1:
            return result[0]
        else:
            raise Exception

    def filter(self, **kwargs):
        """ filter record from db
        
        :param kwargs: filter condition
        :return: result
        
        """
        table_name = self.Meta.table_name
        condition_list = []
        for column_name in kwargs:
            value = kwargs.get(column_name)
            if isinstance(value, str):
                value = "'%s'" % value
            elif isinstance(value, unicode):
                value = value.encode("utf-8")
                value = "'%s'" % value
            elif value is None:
                value = "NULL"
            else:
                value = str(value)
            condition_list.append("%s=%s" % (column_name, value))
        if condition_list:
            condition = " WHERE " + " AND ".join(condition_list)
        else:
            condition = ""
        sql = "SELECT * FROM %s %s" % (table_name, condition)
        result = self.Meta.engine.query_obj(sql, self.__class__.__name__)
        return result

    def create(self):
        pass

    class Meta:
        table_name = None
        engine = None
