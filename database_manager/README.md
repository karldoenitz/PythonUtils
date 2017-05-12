# Database Manager
```
.
├── engine.py     orm引擎
├── fields.py     fields模块
├── model.py      model模块
├── utils.py      工具模块
├── mysql_dbm     MySQL
├── postgre_dbm   postgreSQL
└── sqlite_dbm    sqLite
```
# Usage
```python
# -*- coding: utf-8 -*-

from database_manager.engine import Engine, EngineName
from database_manager.model import Model
from database_manager.fields import *

__author__ = "karlvorndoenitz@gmail.com"

engine = Engine(
    EngineName.PostGre,
    host="127.0.0.1",
    port=5432,
    user="postgres",
    pwd="test",
    db="test_db"
).create()


class User(Model):
    id = IntegerField(default=0, length=False, prime_key=True, auto_increment=True, index=True)
    user_name = CharField(default="", length=16, index=True)
    age = IntegerField(default=None, length=2, null=True)
    is_vip = BooleanField(default=False, null=False)
    comment = TextField(default="无")
    score = FloatField(default=0.0, null=False, length=16)

    class Meta:
        engine = engine
        table_name = "users"


if __name__ == '__main__':
    print User.create()
    user = User()
    user.user_name = "Ada Wong"
    user.age = 16
    user.is_vip = False
    user.score = 100.0
    user2 = User()
    user2.user_name = "Leon"
    user2.age = 48
    user2.is_vip = True
    user2.score = 0.9
    user3 = User()
    user3.user_name = "Chris"
    user3.age = 48
    user3.is_vip = True
    user3.score = 0.9
    print user.save()
    print user2.save()
    print user3.save()
    for user in User.object().filter("age<48"):
        print user.user_name, user.age, user.is_vip, user.comment, user.score

```
