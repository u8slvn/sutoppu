#!/usr/bin/env python3
# coding: utf-8

import pytest

from sutoppu import Specification
from tests.conftest import (FruitIsBitter, FruitIsSweet, FruitIsYellow, apple,
                            avocado, lemon, orange)


def test_specification_must_have_is_satisfied_by():
    class WrongSpecification(Specification):
        """You must implement is_satisfied_by method."""

    with pytest.raises(TypeError):
        WrongSpecification()


@pytest.mark.parametrize('fruit, expected', [
    (lemon, True),
    (orange, False),
])
def test_satisfied_specification(fruit, expected):
    result = FruitIsYellow().is_satisfied_by(fruit)

    assert result is expected


@pytest.mark.parametrize('fruit, expected', [
    (lemon, True),
    (orange, False),
])
def test_satisfied_callable_specification(fruit, expected):
    specification = FruitIsYellow()

    result = specification(fruit)

    assert result is expected


@pytest.mark.parametrize('fruit, expected', [
    (lemon, False),
    (orange, True),
    (apple, False),
])
def test_and_specification(fruit, expected):
    specification = FruitIsSweet() & FruitIsBitter()
    result = specification.is_satisfied_by(fruit)

    assert result is expected


@pytest.mark.parametrize('fruit, expected', [
    (lemon, True),
    (orange, True),
    (avocado, False),
])
def test_or_specification(fruit, expected):
    specification = FruitIsSweet() | FruitIsBitter()

    result = specification.is_satisfied_by(fruit)

    assert result is expected


@pytest.mark.parametrize('fruit, expected', [
    (lemon, False),
    (orange, False),
    (apple, True),
])
def test_not_specification(fruit, expected):
    specification = ~ FruitIsBitter()

    result = specification.is_satisfied_by(fruit)

    assert result is expected


@pytest.mark.parametrize('fruit, expected', [
    (lemon, False),
    (orange, True),
    (apple, False),
    (avocado, True),
])
def test_chain_specification(fruit, expected):
    specification = (FruitIsBitter() & ~FruitIsYellow()) \
                    | (~ FruitIsBitter() & ~FruitIsSweet())

    result = specification.is_satisfied_by(fruit)

    assert result is expected


def test_repr():
    specification = FruitIsYellow()
    expected = '<FruitIsYellow: Fruit must be yellow.>'
    assert expected == f'{specification!r}'
