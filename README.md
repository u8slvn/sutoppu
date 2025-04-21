# Sutoppu

[![Pypi Version](https://img.shields.io/pypi/v/sutoppu.svg)](https://pypi.org/project/sutoppu/)
[![Python Version](https://img.shields.io/pypi/pyversions/sutoppu)](https://pypi.org/project/sutoppu/)
[![CI](https://github.com/u8slvn/sutoppu/actions/workflows/ci.yml/badge.svg)](https://github.com/u8slvn/sutoppu/actions/workflows/ci.yml)
[![Coverage Status](https://coveralls.io/repos/github/u8slvn/sutoppu/badge.svg?branch=master)](https://coveralls.io/github/u8slvn/sutoppu?branch=master)
[![Project license](https://img.shields.io/pypi/l/sutoppu)](https://pypi.org/project/sutoppu/)

**Sutoppu** (ストップ - Japanese from English *Stop*) is a lightweight implementation of the Specification pattern for Python, enabling elegant business rule composition through boolean logic.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Core Concepts](#core-concepts)
- [Basic Usage](#basic-usage)
- [Advanced Features](#advanced-features)
  - [Combining Specifications](#combining-specifications)
  - [Call Syntax](#call-syntax)
  - [Error Reporting](#error-reporting)
- [Real-World Examples](#real-world-examples)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Specification pattern is a powerful approach for encapsulating business rules in reusable, combinable objects. This pattern is especially valuable in domain-driven design and applications with complex validation logic.

Sutoppu brings this pattern to Python with a clean, intuitive API that leverages Python's operator overloading to create natural boolean expressions for your business rules.

> "In computer programming, the specification pattern is a particular software design pattern, whereby business rules can be recombined by chaining the business rules together using boolean logic. The pattern is frequently used in the context of domain-driven design." – [Wikipedia](https://en.wikipedia.org/wiki/Specification_pattern)

See [original paper](https://www.martinfowler.com/apsupp/spec.pdf) by Eric Evans and Martin Fowler for more information.

## Installation

```sh
pip install sutoppu
```

Sutoppu is compatible with Python 3.8+ and has no external dependencies for Python 3.11+. For Python 3.8-3.10, it requires only the lightweight typing-extensions package.

## Core Concepts

The foundation of Sutoppu is the `Specification` abstract base class, which:

1. Defines a contract for checking if an object satisfies a specific rule
2. Provides operators for combining specifications using boolean logic
3. Includes built-in error tracking to identify which rules aren't satisfied

Each specification must implement the `is_satisfied_by(candidate)` method, which returns `True` if the candidate meets the specification's criteria or `False` otherwise.

## Basic Usage

Here's a simple example demonstrating how to create and use specifications:

```python
from sutoppu import Specification


# Define a domain entity
class User:
    def __init__(self, username: str, email: str, age: int) -> None:
        self.username = username
        self.email = email
        self.age = age


# Create specifications for user validation
class ValidUsername(Specification[User]):
    description = "Username must be between 3 and 20 characters."

    def is_satisfied_by(self, user: User) -> bool:
        return 3 <= len(user.username) <= 20


class ValidEmail(Specification[User]):
    description = "Email must contain @ symbol."

    def is_satisfied_by(self, user: User) -> bool:
        return "@" in user.email


class AdultUser(Specification[User]):
    description = "User must be 18 or older."

    def is_satisfied_by(self, user: User) -> bool:
        return user.age >= 18


# Use the specifications
user1 = User("john_doe", "john@example.com", 25)
user2 = User("jo", "invalid-email", 17)

# Combine specifications
valid_user = ValidUsername() & ValidEmail() & AdultUser()

# Check if users are valid
print(valid_user.is_satisfied_by(user1))  # True
print(valid_user.is_satisfied_by(user2))  # False

# Check which rules failed
valid_user.is_satisfied_by(user2)
print(valid_user.errors)

# {
#    'ValidUsername': 'Username must be between 3 and 20 characters.',
#    'ValidEmail': 'Email must contain @ symbol.',
#    'AdultUser': 'User must be 18 or older.'
# }
```

## Advanced Features

### Combining Specifications

Sutoppu overloads Python's bitwise operators to create a natural, expressive syntax for combining specifications:

- `&` (AND): Both specifications must be satisfied
- `|` (OR): At least one specification must be satisfied
- `~` (NOT): The specification must not be satisfied

These operators can be chained to create complex rule compositions:

```python
# User must be an adult with valid credentials, OR an approved minor
valid_account = (ValidUsername() & ValidEmail() & AdultUser()) | ApprovedMinor()

# User must have valid credentials but must NOT be blacklisted
active_account = (ValidUsername() & ValidEmail()) & ~Blacklisted()
```

### Call Syntax

For a more concise syntax, specifications can be called directly as functions:

```python
adult_user = AdultUser()

# These are equivalent:
result1 = adult_user.is_satisfied_by(user)
result2 = adult_user(user)
```

### Error Reporting

Sutoppu automatically tracks which specifications fail during validation. After checking a candidate, the `errors` dictionary provides detailed feedback on each failed rule:

```python
complex_spec = SpecA() & (SpecB() | SpecC()) & ~SpecD()
complex_spec.is_satisfied_by(candidate)

if complex_spec.errors:
    for spec_name, description in complex_spec.errors.items():
        print(f"Failed rule: {spec_name} - {description}")
```

Key features of error reporting:

- The `errors` dictionary is reset before each validation
- Keys are specification class names
- Values are the descriptions defined in the specifications
- Negated specifications that fail show "Expected condition to NOT satisfy: [original description]" as description

## Real-World Examples

### Product Eligibility for Promotion

```python
from sutoppu import Specification
from datetime import datetime, timedelta
from typing import Set, Literal


# Define allowed category types for better type checking
CategoryType = Literal["electronics", "home", "fashion", "books", "toys", "sports"]


class Product:
    def __init__(
        self,
        sku: str,
        category: CategoryType,
        price: float,
        created_at: datetime,
        stock: int,
    ) -> None:
        self.sku = sku
        self.category = category
        self.price = price
        self.created_at = created_at
        self.stock = stock


class InPromotionCategory(Specification[Product]):
    description = "Product must be in eligible promotion category."
    PROMO_CATEGORIES: Set[CategoryType] = {"electronics", "home", "fashion"}

    def is_satisfied_by(self, product: Product) -> bool:
        return product.category in self.PROMO_CATEGORIES


class PriceThreshold(Specification[Product]):
    description = "Product must cost at least $50."

    def is_satisfied_by(self, product: Product) -> bool:
        return product.price >= 50.0


class NewArrival(Specification[Product]):
    description = "Product must be added within the last 30 days."

    def is_satisfied_by(self, product: Product) -> bool:
        days_since_added = (datetime.now() - product.created_at).days
        return days_since_added <= 30


class InStock(Specification[Product]):
    description = "Product must be in stock."

    def is_satisfied_by(self, product: Product) -> bool:
        return product.stock > 0


# Combine specifications for promotion eligibility
promotion_eligible = (
    InPromotionCategory() &
    PriceThreshold() &
    (NewArrival() | ~InStock())  # New arrivals or out-of-stock products
)

# Example products
eligible_product = Product(
    sku="ELEC123",
    category="electronics",
    price=199.99,
    created_at=datetime.now() - timedelta(days=5),  # 5 days ago
    stock=10
)

ineligible_product = Product(
    sku="BOOK789",
    category="books",
    price=14.99,
    created_at=datetime.now() - timedelta(days=60),  # 60 days ago
    stock=20
)

# Check eligibility for both products
is_eligible = promotion_eligible.is_satisfied_by(eligible_product)
print(f"Electronics product eligible for promotion: {is_eligible}")

# Electronics product eligible for promotion: True

is_ineligible = promotion_eligible.is_satisfied_by(ineligible_product)
print(f"Book eligible for promotion: {is_ineligible}")

# Book eligible for promotion: False

# Display failure reasons for the ineligible product
print("Failure reasons:", promotion_eligible.errors)

# Failure reasons:: {
#   'InPromotionCategory': 'Product must be in eligible promotion category.',
#   'PriceThreshold': 'Product must cost at least $50.',
#   'NewArrival': 'Product must be added within the last 30 days.',
#   'InStock': 'Expected condition to NOT satisfy: Product must be in stock.'
# }
```

### User Permission System

```python
from sutoppu import Specification
from typing import List, Set, Literal, Union


# Define domain types
RoleType = Literal["admin", "user", "manager", "auditor"]
DepartmentType = Literal["IT", "HR", "Finance", "Marketing", "Operations"]


class User:
    def __init__(
        self,
        roles: Set[RoleType],
        department: DepartmentType,
        access_level: int,
        two_factor_enabled: bool,
    ) -> None:
        self.roles = roles
        self.department = department
        self.access_level = access_level
        self.two_factor_enabled = two_factor_enabled


class AdminRole(Specification[User]):
    description = "User must have admin role."

    def is_satisfied_by(self, user: User) -> bool:
        return "admin" in user.roles


class ITDepartment(Specification[User]):
    description = "User must be in IT department."

    def is_satisfied_by(self, user: User) -> bool:
        return user.department == "IT"


class SeniorAccessLevel(Specification[User]):
    description = "User must have senior access level."
    SENIOR_THRESHOLD: int = 7

    def is_satisfied_by(self, user: User) -> bool:
        return user.access_level >= self.SENIOR_THRESHOLD


class TwoFactorEnabled(Specification[User]):
    description = "User must have 2FA enabled."

    def is_satisfied_by(self, user: User) -> bool:
        return user.two_factor_enabled


# Define sensitive data access rule
can_access_sensitive_data = (
    (AdminRole() | (ITDepartment() & SeniorAccessLevel())) &
    TwoFactorEnabled()
)

# Example check with a regular user
regular_user = User(
    roles={"user"},
    department="Finance",
    access_level=6,
    two_factor_enabled=True
)

# Check permission
has_access = can_access_sensitive_data.is_satisfied_by(regular_user)
print(f"Regular user can access sensitive data: {has_access}")

# Regular user can access sensitive data: False

# Check which rules failed
print("Failed rules:", can_access_sensitive_data.errors)

# Failed rules: {
#   'AdminRole': 'User must have admin role.',
#   'ITDepartment': 'User must be in IT department.',
#   'SeniorAccessLevel': 'User must have senior access level.'
# }
```

## API Reference

### `Specification[T]`

Abstract base class for creating specifications. Type parameter `T` defines the type of objects being checked.

**Attributes:**

- `description`: Class attribute for describing the rule (default: "No description provided.")
- `errors`: Dictionary of failed specifications, with class names as keys and descriptions as values

**Methods:**

- `is_satisfied_by(candidate: T) -> bool`: Abstract method that must be implemented by concrete specifications
- `__and__(other: Specification[T]) -> Specification[T]`: Combine with another specification using AND logic
- `__or__(other: Specification[T]) -> Specification[T]`: Combine with another specification using OR logic
- `__invert__() -> Specification[T]`: Negate the specification (NOT logic)
- `__call__(candidate: T) -> bool`: Shorthand for calling `is_satisfied_by()`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -am 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/u8slvn/sutoppu/blob/master/LICENSE) file for details.
