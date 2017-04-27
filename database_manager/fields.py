# -*-encoding:utf-8-*-

__author__ = "karlvorndoenitz@gmail.com"


TypeMapping = {
    "IntegerField": "INTEGER",
    "BooleanField": "BOOLEAN",
    "CharField": "VARCHAR",
    "FloatField": "FLOAT",
    "TextField": "TEXT"
}


class Field(object):
    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs

    def to_create(self, col_name):
        tp = TypeMapping[self.__class__.__name__]
        create_lan = [col_name]
        default_val = self.kwargs.get("default")
        value = ""
        if self.kwargs.get("length"):
            create_lan.append(tp + ("(%d)" % self.kwargs.get("length")))
        else:
            create_lan.append(tp)
        if self.kwargs.get("null"):
            create_lan.append("NULL")
        else:
            create_lan.append("NOT NULL")
        if self.kwargs.get("blank"):
            create_lan.append("")
        if self.kwargs.get("prime_key"):
            create_lan.append("PRIMARY KEY")
        if self.kwargs.get("auto_increment"):
            create_lan.append("AUTOINCREMENT")
        if isinstance(default_val, int) or isinstance(default_val, float):
            value = "DEFAULT %s" % str(default_val)
        elif isinstance(default_val, bool):
            value = "DEFAULT TRUE" if default_val else "DEFAULT FALSE"
        elif isinstance(default_val, str):
            value = "DEFAULT '%s'" % default_val
        elif default_val is None:
            value = "DEFAULT NULL"
        create_lan.append(value)
        return " ".join(create_lan)


class IntegerField(Field):
    def __init__(self, default, length, null=False, blank=False, prime_key=False, index=False, auto_increment=False):
        super(IntegerField, self).__init__(
            default=default,
            null=null,
            blank=blank,
            prime_key=prime_key,
            index=index,
            length=length,
            auto_increment=auto_increment
        )


class BooleanField(Field):
    def __init__(self, default, null=False, blank=False, prime_key=False, index=False):
        super(BooleanField, self).__init__(
            default=default,
            null=null,
            blank=blank,
            prime_key=prime_key,
            index=index
        )


class CharField(Field):
    def __init__(self, default, length, null=False, blank=False, prime_key=False, index=False):
        super(CharField, self).__init__(
            default=default,
            null=null,
            blank=blank,
            prime_key=prime_key,
            index=index,
            length=length
        )


class FloatField(Field):
    def __init__(self, default, length, null=False, blank=False, prime_key=False, index=False):
        super(FloatField, self).__init__(
            default=default,
            null=null,
            blank=blank,
            prime_key=prime_key,
            index=index,
            length=length
        )


class TextField(Field):
    def __init__(self, default, null=False, blank=False, prime_key=False, index=False):
        super(TextField, self).__init__(
            default=default,
            null=null,
            blank=blank,
            prime_key=prime_key,
            index=index
        )
