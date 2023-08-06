cf-json
#######

**Expanded JSON serialization**

.. Project Links

     * `PYPI <https://https://pypi.org/project/cf-json/>`_
     * `Documentation <https://cf-json.readthedocs.io/en/latest>`_
     * `Gitlab <https://gitlab.clayfox.co.nz/keir/cf-json>`_
     * `Bug Tracker <https://gitlab.clayfox.co.nz/keir/cf-json/-/issues>`_

#######

Summary
-------

``cf-json`` provides a batteries included approach to extending the standard `json` module.


It achieves this by making use of a custom `json.JSONEncoder` subclass `cfjson.MyEncoder` to
expand the range of types that can be serialized. While keeping sticking to the `json` interface.


Installation
------------

Install the package from `PyPI <https://pypi.org/project/cf-json/>`_:

.. code-block:: console

    $ python -m pip install cf-json
    [...]
    Successfully installed cf-json


Quick Start
-----------

`cf-json` is a drop in replacement for the standard `json` module.

.. code-block:: python

    >>> from cfjson import dumps, loads
    >>> data = {1: 'a', 2: Path('./my_file.py'), 3: datetime.datetime.utcnow()}
    >>> data
    {1: 'a', 2: WindowsPath('my_file.py'), 3: datetime.datetime(2021, 4, 7, 2, 45, 57, 696066)}
    >>> json_blob = dumps(data)
    >>> json_blob
    '{"1": "a", "2": {"__json_type__": "WindowsPath", "path": "my_file.py"}, "3": {"__json_type__": "datetime", "datetime": "2021-04-07T02:45:57.696066"}}'
    >>> loads(json_blob)
    {'1': 'a', '2': WindowsPath('my_file.py'), '3': datetime.datetime(2021, 4, 7, 2, 45, 57, 696066)}

Documentation
-------------

`Full documentation <https://cf-json.readthedocs.io/en/latest>`_