# Jata - Typed Json Data

Simple class to convert to and from json with benefits of IDE autocomplete. 
Designed primarily for using Json web APIs directly without an unnecessary wrapper client.
See example.py for usage

## Features

* Allows to declare types and defaults in class definition
* No restriction on the order of default and non-default fields even for inherited fields
* Does no validation, all fields are optional and can be set later
* Allows python keywords as fields with `pykw_` prefix. The prefix is automatically removed/added on json conversion
* Does not care about extra unexpected fields. They just silently exist. Beware of typhos!


## TODO

* Tool for generating constructor stubs (They don't work for IDE autocomplete)
* Tool for generating class from a sample json
* unit tests
* write doc - Using StrEnum, constructor example, Comparison table
* Continuous integration
* Optionally do validation before serializing

## Related

* [dataclass](https://docs.python.org/3/library/dataclasses.html)
* [namedtuple](https://docs.python.org/3/library/collections.html#collections.namedtuple)
* [NamedTuple](https://docs.python.org/3/library/typing.html#typing.NamedTuple)
* [TypedDict](https://docs.python.org/3/library/typing.html#typing.TypedDict)
* [attrs](https://www.attrs.org)
* [Box](https://github.com/cdgriffith/Box)
* [dacite](https://github.com/konradhalas/dacite)
* [pydantic](https://github.com/samuelcolvin/pydantic)
