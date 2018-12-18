# Sutoppu

[![Build Status](https://travis-ci.org/u8slvn/sutoppu.svg?branch=master)](https://travis-ci.org/u8slvn/sutoppu)
[![Coverage Status](https://coveralls.io/repos/github/u8slvn/sutoppu/badge.svg?branch=master)](https://coveralls.io/github/u8slvn/sutoppu?branch=master)

**Sutoppu** (ストップ from English *Stop*) is a simple python implementation of Specification pattern.

## What is Specification Pattern?

See [Wikipedia](https://en.wikipedia.org/wiki/Specification_pattern).

> In computer programming, the specification pattern is a particular software design pattern, whereby business rules can be recombined by chaining the business rules together using boolean logic. The pattern is frequently used in the context of domain-driven design.

## Basic usage

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
    def is_satisfied_by(self, fruit):
        return fruit.bitter is True


class FruitIsSweet(Specification):
    def is_satisfied_by(self, fruit):
        return fruit.sweet is True


class FruitIsYellow(Specification):
    def is_satisfied_by(self, fruit):
        return fruit.color == 'yellow'


lemon = Fruit(color='yellow', sweet=False, bitter=True)

# Apply your specifications
is_a_lemon = FruitIsYellow().and_(FruitIsBitter().and_not(FruitIsSweet()))

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

---

For more information: [Eric Evans and Martin Fowler article about Specifications](https://www.martinfowler.com/apsupp/spec.pdf)
