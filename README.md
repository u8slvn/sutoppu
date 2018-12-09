# Sutoppu

[![Build Status](https://travis-ci.org/u8slvn/sutoppu.svg?branch=master)](https://travis-ci.org/u8slvn/sutoppu)

**Sutoppu** (ストップ from English *Stop*) is a simple python implementation of Specification pattern.

## What is Specification Pattern?

See [Wikipedia](https://en.wikipedia.org/wiki/Specification_pattern).

> In computer programming, the specification pattern is a particular software design pattern, whereby business rules can be recombined by chaining the business rules together using boolean logic. The pattern is frequently used in the context of domain-driven design.

## Example of use

### Basic usage

```python
from sutoppu import Specification


class Fruit:
    def __init__(self, color, sweetened, sour):
        self.color = color
        self.sweetened = sweetened
        self.sour = sour


# Define your domain specifications
class FruitIsALemon(Specification):
    def is_satisfied_by(self, fruit):
        return fruit.color == 'yellow' \
               and fruit.sweetened is False \
               and fruit.sour is True


lemon = Fruit(color='yellow', sweetened=False, sour=True)

# Apply your specifications
if FruitIsYellow().is_satisfied_by(lemon):
    print('This is a lemon!')
else:
    print('This is not a lemon!')
```

### Statements

#### `and_`

```python
my_spec = SpecificationA().and_(SpecificationB())
```

#### `and_not`

```python
my_spec = SpecificationA().and_not(SpecificationB())
```

#### `or_`

```python
my_spec = SpecificationA().or_(SpecificationB())
```

#### `or_not`

```python
my_spec = SpecificationA().or_not(SpecificationB())
```

#### `not_`

```python
my_spec = SpecificationA().not_()
```

---

For more information: [Eric Evans and Martin Fowler article about Specifications](https://www.martinfowler.com/apsupp/spec.pdf)
