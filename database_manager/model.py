# -*-encoding:utf-8-*-
"""

model
~~~~~~

introduction
this module is the base module of ORM.

Usage
=====
>>> from database_manager.fields import CharField, IntegerField
>>> class Character(Model):
...     name = CharField(default="", null=False, length=16)
...     age = IntegerField(default=None, null=True, length=3)
...     class Meta:
...         table_name = "character"
... 
>>> # SELECT * FROM character WHERE age > 10 AND name='Ada Wong';
>>> for character in Character.object().filter("age>10", name="Ada Wong"):
...     print character.name, character.age
...

"""

import time
from utils import object_to_dict, obj_field_to_dict

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

    def filter(self, *args, **kwargs):
        """ filter record from db
        
        :param args: filter condition
        :param kwargs: filter condition
        :return: result
        
        """
        table_name = self.Meta.table_name
        condition_list = [] + list(args)
        for column_name in kwargs:
            value = kwargs.get(column_name)
            if isinstance(value, str):
                value = "'%s'" % value
            elif isinstance(value, bool):
                value = "1" if value else "0"
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

    def update(self, *args, **kwargs):
        """ update record in db

        :param args: filter condition
        :param kwargs: filter condition
        :return: result

        """
        attr_dict = object_to_dict(self)
        value_list = []
        for key in attr_dict:
            value = attr_dict[key]
            if isinstance(value, str):
                value = "'%s'" % value
            elif isinstance(value, unicode):
                value = value.encode("utf-8")
                value = "'%s'" % value
            elif value is None:
                value = "NULL"
            else:
                value = str(value)
            value_list.append("%s=%s" % (key, value))
        table_name = self.Meta.table_name
        condition_list = [] + list(args)
        for column_name in kwargs:
            value = kwargs.get(column_name)
            if isinstance(value, str):
                value = "'%s'" % value
            elif isinstance(value, bool):
                value = "1" if value else "0"
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
        elif hasattr(self, "id") and getattr(self, "id"):
            condition = " WHERE id=%s" % str(getattr(self, "id"))
        else:
            condition = ""
        sql = "UPDATE %s SET %s %s" % (table_name, ",".join(value_list), condition)
        return self.Meta.engine.execute(sql)

    def all(self):
        """ get all data from database table
        
        :return: data
        
        """
        sql = "SELECT * FROM %s" % self.Meta.table_name
        result = self.Meta.engine.query_obj(sql, self.__class__.__name__)
        return result

    def delete(self, *args, **kwargs):
        """ delete from table

        :param args: delete condition
        :param kwargs: delete condition
        :return: de

        """
        condition = ""
        if kwargs:
            condition_list = [] + list(args)
            for column_name in kwargs:
                value = kwargs.get(column_name)
                if isinstance(value, str):
                    value = "'%s'" % value
                elif isinstance(value, bool):
                    value = "1" if value else "0"
                elif isinstance(value, unicode):
                    value = value.encode("utf-8")
                    value = "'%s'" % value
                elif value is None:
                    value = "NULL"
                else:
                    value = str(value)
                condition_list.append("%s=%s" % (column_name, value))
            condition += ", ".join(condition_list)
        if condition:
            sql = "DELETE FROM %s WHERE %s" % (self.Meta.table_name, condition)
        else:
            sql = "DELETE FROM %s WHERE id=%d" % (self.Meta.table_name, self.id)
        return self.Meta.engine.execute(sql)

    @classmethod
    def create(cls):
        """ create the table in database
        
        :return: True or exception
        
        """
        try:
            obj_field_dict = obj_field_to_dict(cls)
            sql = "(%s)" % ",".join(
                [obj_field_dict[key].to_create(cls.Meta.engine.engine_name, key) for key in obj_field_dict]
            )
            create_sql = "CREATE TABLE %s %s" % (cls.Meta.table_name, sql)
            cls.Meta.engine.execute(create_sql)
            for key in obj_field_dict:
                index_name = "%s_%d" % (key, time.time()*1000)
                if obj_field_dict.get(key).kwargs.get("index"):
                    unique = "UNIQUE" if obj_field_dict.get(key).kwargs.get("unique") else ""
                    create_index_sql = "CREATE %s INDEX %s ON %s (%s)" % (unique, index_name, cls.Meta.table_name, key)
                    cls.Meta.engine.execute(create_index_sql)
            return True
        except Exception, e:
            raise e

    @classmethod
    def object(cls):
        return cls()

    class Meta:
        table_name = None
        engine = None
