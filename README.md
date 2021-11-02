# Sutoppu

[![Pypi Version](https://img.shields.io/pypi/v/sutoppu.svg)](https://pypi.org/project/sutoppu/)
[![Python Version](https://img.shields.io/pypi/pyversions/sutoppu)](https://pypi.org/project/sutoppu/)
[![CI](https://github.com/u8slvn/sutoppu/actions/workflows/ci.yml/badge.svg)](https://github.com/u8slvn/sutoppu/actions/workflows/ci.yml)
[![Coverage Status](https://coveralls.io/repos/github/u8slvn/sutoppu/badge.svg?branch=master)](https://coveralls.io/github/u8slvn/sutoppu?branch=master)
[![Project license](https://img.shields.io/pypi/l/sutoppu)](https://pypi.org/project/sutoppu/)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Sutoppu** (ストップ - Japanese from English *Stop*) is a simple python implementation of Specification pattern.

## What is Specification Pattern?

See [Wikipedia](https://en.wikipedia.org/wiki/Specification_pattern).

> In computer programming, the specification pattern is a particular software design pattern, whereby business rules can be recombined by chaining the business rules together using boolean logic. The pattern is frequently used in the context of domain-driven design.

More information: [Eric Evans and Martin Fowler article about Specifications](https://www.martinfowler.com/apsupp/spec.pdf)

## Basic usage

### Installation

```sh
$ pip install sutoppu
```

### Usage

```python
from sutoppu import Specification


class Fruit:
    def __init__(self, color: str, sweet: bool, bitter: bool):
        self.color = color
        self.sweet = sweet
        self.bitter = bitter


class FruitIsBitter(Specification):
    description = 'The given fruit must be bitter.'

    def is_satisfied_by(self, fruit: Fruit):
        return fruit.bitter is True


class FruitIsSweet(Specification):
    description = 'The given fruit must be sweet.'
    
    def is_satisfied_by(self, fruit: Fruit):
        return fruit.sweet is True


class FruitIsYellow(Specification):
    description = 'The given fruit must be yellow.'

    def is_satisfied_by(self, fruit: Fruit):
        return self.color == 'yellow'
```

```python
>>> lemon = Fruit(color='yellow', sweet=False, bitter=True)
>>> is_a_lemon = FruitIsYellow() & FruitIsBitter() & ~FruitIsSweet()
>>> is_a_lemon.is_satisfied_by(lemon)
True
```

### Operators

Bitwise operators are overload to provide simple syntax.

And:
yellow
```python
>>> my_spec = SpecificationA() & SpecificationB()
```

Or:

```python
>>> my_spec = SpecificationA() | SpecificationB()
```

Not:

```python
>>> my_spec = ~SpecificationA()
```

### Lighter syntax

If you do not find the `is_satisfied_by` method very convenient you can also directly call the specification as below.

```python
>>> lemon = Fruit(color='yellow', sweet=False, bitter=True)
>>> is_a_lime = FruitIsGreen() & FruitIsBitter() & ~FruitIsSweet()
>>> is_a_lime(lemon)
False
```

### Error reporting

It can be difficult to know which specification failed in a complex rule. Sutoppu allows to list all the failed specifications by getting the `errors` attribute after use.
The `errors` attribute is reset each time the specification is used. For each failed specification, it returns a dict with the name of the specification class for key and the description provide in the class for value. In the case where the specification failed with a `not` condition, the description is prefixed with `Not ~`.

```python
>>> apple = Fruit(color='red', sweet=True, bitter=False)
>>> is_a_lemon = FruitIsYellow() & FruitIsBitter() & ~ FruitIsSweet()
>>> is_a_lemon.is_satisfied_by(apple)
False
>>> is_a_lemon.errors
{
    'FruitIsColored': 'The given fruit must be yellow.',
    'FruitIsBitter': 'The given fruit must be bitter.',
    'FruitIsSweet': 'Not ~ The given fruit must be sweet.'
}
```
