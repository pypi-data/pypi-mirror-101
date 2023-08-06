# Breaking Version Changes

## 6.1.0
* The new lazy settings need a `src/config.py` file or you need to set the `SETTINGS_MODULE` environment variable to a module

## 6.0.0

* All `OpenModuleModel` fields of type `datetime` require a timezone validator which is checked during testing /
  debugging. After this version **all datetime objects should be timezone naive**.
* All sqlalchemy database models disallow the use of `DateTime` and require the use of `TZDateTime`. This preemptively
  avoids bugs, because sqlalchemy with sqlite looses timezone information.
* `models.backend.Access` now uses timezone naive datetimes instead of timezone aware datetimes. The `is_valid` method
  still accepts both.
* in MessageDispatcher `raise_validation_errors` and `raise_handler_errors` are now required to be named arguments
* `MockEvent.wait_for_call()` now raises a Timeout error instead of an assertion error

## 5.0.0

* AlertHandler.send() and get_or_add_alert_id() were refactored:
    * `source` is now a keyword argument, with default value `""`
    * most arguments are forced to keyword arguments

## 4.0.0

* the Category Enum was renamed to AccessCategory
* all member variables of Category/AccessCategory are lowercased
* the Medium Enum was renamed to MediumType
* all member variables of Medium/MediumType are lowercased
* the default database folder changed to a mounted volume

## 3.0.0

* the registration of bases for the database changed from `register_bases([...])` to `run_env_py([...])`

## 2.0.0

* Pydantic models are now defined in a model folder