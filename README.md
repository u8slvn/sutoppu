# Sutoppu

[![Build Status](https://travis-ci.org/u8slvn/sutoppu.svg?branch=master)](https://travis-ci.org/u8slvn/sutoppu)
[![Coverage Status](https://coveralls.io/repos/github/u8slvn/sutoppu/badge.svg?branch=master)](https://coveralls.io/github/u8slvn/sutoppu?branch=master)
[![Pypi Version](https://img.shields.io/pypi/v/sutoppu.svg)](https://pypi.org/project/sutoppu/)

**Sutoppu** (ストップ - Japanese from English *Stop*) is a simple python implementation of Specification pattern.

## What is Specification Pattern?

See [Wikipedia](https://en.wikipedia.org/wiki/Specification_pattern).

> In computer programming, the specification pattern is a particular software design pattern, whereby business rules can be recombined by chaining the business rules together using boolean logic. The pattern is frequently used in the context of domain-driven design.

## Basic usage

### Install

```bash
$ pip install sutoppu
```

### Example

```python
from sutoppu import Specification


class Fruit:
    def __init__(self, color, sweet, bitter):
        self.color = color
        self.sweet = sweet
        self.bitter = bitter


# Define your domain specifications
class FruitIsBitter(Specification):
    def _is_satisfied_by(self, fruit):
        return fruit.bitter is True


class FruitIsSweet(Specification):
    def _is_satisfied_by(self, fruit):
        return fruit.sweet is True


class FruitIsColored(Specification):
    def __init__(self, color):
        super().__init__()  # do not forget super()
        self.color = color

    def _is_satisfied_by(self, fruit):
        return self.color == fruit.color


lemon = Fruit(color='yellow', sweet=False, bitter=True)

# build your specifications
is_a_lemon = FruitIsColored('yellow').and_(FruitIsBitter().and_not(FruitIsSweet()))

# apply your specification
if is_a_lemon.is_satisfied_by(lemon):
    print('This is a lemon!')
else:
    print('This is not a lemon!')
```

### Operators

```python
# and_
my_spec = SpecificationA().and_(SpecificationB())

# and_not
my_spec = SpecificationA().and_not(SpecificationB())

# or_
my_spec = SpecificationA().or_(SpecificationB())

# or_not
my_spec = SpecificationA().or_not(SpecificationB())

# not_
my_spec = SpecificationA().not_()
```

## Extra syntax

For lighter declarations you can also use bitwise operators.

```python
# and
my_spec = SpecificationA() & SpecificationB()

# or
my_spec = SpecificationA() | SpecificationB()

# not
my_spec = ~ SpecificationA()
```

### Example

```python
from somerules import FruitIsYellow, FruitIsBitter, FruitIsSweet
from fruits import apple

# we want a sweet non yellow fruit or a bitter fruit
my_spec = (FruitIsSweet() & ~ FruitIsYellow()) | FruitIsBitter()

if my_spec.is_satisfied_by(apple):
    print('I want to eat that fruit!')
```

## Error report

It can be difficult to know which specification failed in a complex rule. Sutoppu allows to list all the failed verifications by getting the `errors` attribute after a specification use.
The `errors` attribute is reset each time the specification is used. For each failed specification, it returns a dict with the name of the specification class for key and the description provide in the class for value. In the case where the specification failed with a `not` condition, the description are prefixed with `Not ~`.

### Example

```python
from sutoppu import Specification
import Fruit


class FruitIsBitter(Specification):
    description = 'The given fruit must be bitter.'

    def _is_satisfied_by(self, fruit):
        return fruit.bitter is True


class FruitIsSweet(Specification):
    description = 'The given fruit must be sweet.'

    def _is_satisfied_by(self, fruit):
        return fruit.sweet is True


class FruitIsColored(Specification):
    description = 'The given fruit must be {color}.'
    
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.description = self.description.format(color=color)

    def _is_satisfied_by(self, fruit):
        return self.color == fruit.color


apple = Fruit(color='red', sweet=True, bitter=False)

is_a_lemon = FruitIsColored('yellow') & FruitIsBitter() & ~ FruitIsSweet()

if is_a_lemon.is_satisfied_by(apple):
    print('A lemon!')

print(is_a_lemon.errors)

# >>> {'FruitIsColored': 'The given fruit must be yellow.',
#      'FruitIsBitter': 'The given fruit must be bitter.',
#      'FruitIsSweet': 'Not ~ The given fruit must be sweet.'}
```

---

For more information: [Eric Evans and Martin Fowler article about Specifications](https://www.martinfowler.com/apsupp/spec.pdf)
