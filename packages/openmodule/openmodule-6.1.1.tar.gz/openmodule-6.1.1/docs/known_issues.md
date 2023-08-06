# Known Issues

Similar to the changelog, we write a list of known issues here, so it is easy to identify issues for a particular
version. The changelog may contain many other notes aswell.

The version numbers below always note the _version through which the issue was fixed_.

## 6.0.1

### assertion on start, in production

The library raised an exception when imported in a production environment.

## 6.0.0

### Database Datetime issues

The `DateTime` column type of sqlalchemy looses all timezone information. This can lead to bugs if the datetimes were
not converted to utc/fixed timezone before saving

### `.timestamp()` can cause issues during testing

Calling `.timestamp()` on a `datetime` object causes issues. Mostly during testing. The exported timestamp is the
current time, with the timezone of the system. So when testing they are usually off by one hour **except when using
freezegun** which sets the system timezone to utc suddenly.

Since 6.0.0 a util function `datetime_to_timestamp()` exists, which converts both _naive_ and _aware_ datetime objects
to unix timestamps. _Naive_ objects are interpreted as UTC.

## 5.0.1

### Ignored database exceptions

Up until 5.0.1 exceptions during the database's commit were ignored. The database commit was executed in the `__exit__`
method of the `Database contextmanager.

The following code would not have raised an integrity exception, even tough the exception happended in sqlalchemy.

```python
with database() as db:
    db.add(MyModel(id=1))
    db.add(MyModel(id=1))
```

**But** the following code would have raised an exception. As only exceptions inside the `__exit__` function were
ignored.

```python
with database() as db:
    db.add(MyModel(id=1))
    db.add(MyModel(id=1))
    db.flush()
```

### API Urls

Prior to 5.0.1 the `API` class used `urljoin`. This resulted in weird behaviour depending on your configuration:

```python
api = Api("http://example.com/api/v1")
api.post("resource/create/", {})  # -> posts to "http://example.com/api/resource/create/"
```
