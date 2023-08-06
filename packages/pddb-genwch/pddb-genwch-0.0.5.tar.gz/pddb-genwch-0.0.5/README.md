# Using Pandas as database in python

Using Pandas (Parquet) as database in python

# Method

- set_owner
- set_debug
- cols
- filter
- update
- insert
- upsert
- save
- load

# Sample

Table

```python
class User(pddb.pdtbl):
    def init_obj(self) -> dict:
        path = "./data/users.parquet"
        obj = {"uid": {"type": str, "uuid": True, "ignupd": True},
               "usr_cde": {"type": str, "key": True},
               "usr_name": {"type": str}}
        return (obj, path)
```

```python
class Password(pddb.pdtbl):
    def init_obj(self) -> dict:
        path = "./data/passwords.parquet"
        obj = {"uid": {"type": str, "uuid": True, "key": True, "ignupd": True},
               "password": {"type": str, "require": True, "md5": True}}
        return (obj, path)
```

View

```python
class VW_User_Password(pddb.pdvw):
    def init_obj(self) -> dict:
        usr = User()
        pwd = Password()
        cfg = {"source": [{"name": "usr", "tbl": usr}, {"name": "pwd", "tbl": pwd, "join": ["uid"]}],
               "cols": [{"tbl": "usr", "col": "uid"}, {"tbl": "usr", "col": "usr_cde"}, {"tbl": "pwd", "col": "password"}]}
        return cfg
```
