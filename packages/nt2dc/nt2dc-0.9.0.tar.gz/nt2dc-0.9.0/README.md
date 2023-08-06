# nt2dc

> There should be one—and preferably only one—obvious way to do it.
_The zen of Python_

## Python objects

Currently, python offers different ways of modelling a dead-simple objects. The most complex way is simply a plain old python object:

```python
class Complex:
    def __init__(self, real: float = 0.0, imaginary: float = 0.0) -> None:
        self.__real = real
        self.__imaginary = imaginary

    def __set_real(self, value: float) -> None:
        self.__real = value

    def __get_real(self) -> float:
        return self.__real

    real = property(__get_real, __set_real)

    def __set_imaginary(self, value: float) -> None:
        self.__imaginary = value

    def __get_imaginary(self) -> float:
        return self.__imaginary

    imaginary = property(__get_imaginary, __set_imaginary)

    def __repr__(self) -> str:
        return "{} + {}i".format(self.__real, self.__imaginary)
```

## Dataclasses

With newer versions of python 3, the dataclasses have been introduced, that can be created in two ways:

```python
Complex = make_dataclass('Complex', [('real', float), ('imaginary', float)])
```

**or**

```python
@dataclass
class Complex:
    real: float = field()
    imaginary: float = field()
```

Dataclasses are a great way of handling python data in a dead-simple way. Constructor, `__repr__` function, getters, setters and introspection is possible and make it more easy to create a serialization and deserialization engine. They hence can easily be combined with multiple frameworks like sqlalchemy, marshmallow and entire web frameworks like bottle, flask etc. to create rest-ful APIs.

## Named tuples

On the other hand, there are legacy modelling ways like named tuples, that can be create using two ways:

```python
Complex = namedtuple('Complex', ['real', 'imaginary'])
```

**or**

```python
class Complex(NamedTuple):
    real: float
    imaginary: float
```

**Please note**, that the latter has type hints while the former does not support type hinting yet.

NamedTuples are like tuples: A read-only combination of multiple values, just like regular tuples, but each value has a unique name. 

## Conversion

What if, one API provides or requests NamedTuples but you need a dataclass for further processing or vice versa?

This package provides a set of functions for the conversion from one notation (NamedTuple) to the other (Dataclass) and back.

**Please note**, the type hinted variant should be used.

## Licensing

This library is published under BSD-3-Clause license.

## Versioning

This library follows semantic versioning 2.0. Any breaking change will produce a new major release. Versions below 1.0 are considered to have a unstable interface.
