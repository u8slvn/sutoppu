#!/usr/bin/env python3
# coding: utf-8

import pytest

from tests import Fruit, FruitIsSweet, FruitIsSour, FruitIsYellow

lemon = Fruit(color='yellow', sweet=False, sour=True)
orange = Fruit(color='orange', sweet=True, sour=True)
apple = Fruit(color='red', sweet=True, sour=False)
avocado = Fruit(color='green', sweet=False, sour=False)


class TestSutoppu:
    @pytest.mark.parametrize('fruit, expected', [
        (lemon, True),
        (orange, False),
    ])
    def test_satisfied_specification(self, fruit, expected):
        result = FruitIsYellow().is_satisfied_by(fruit)

        assert result is expected

    @pytest.mark.parametrize('fruit, expected', [
        (lemon, False),
        (orange, True),
        (apple, False),
    ])
    def test_and_specification(self, fruit, expected):
        specification = FruitIsSweet().and_(FruitIsSour())
        result = specification.is_satisfied_by(fruit)

        assert result is expected

    @pytest.mark.parametrize('fruit, expected', [
        (lemon, False),
        (orange, False),
        (apple, True),
    ])
    def test_and_not_specification(self, fruit, expected):
        specification = FruitIsSweet().and_not(FruitIsSour())
        result = specification.is_satisfied_by(fruit)

        assert result is expected

    @pytest.mark.parametrize('fruit, expected', [
        (lemon, True),
        (orange, True),
        (avocado, False),
    ])
    def test_or_specification(self, fruit, expected):
        specification = FruitIsSweet().or_(FruitIsSour())

        result = specification.is_satisfied_by(fruit)

        assert result is expected

    @pytest.mark.parametrize('fruit, expected', [
        (lemon, False),
        (orange, True),
        (apple, True),
    ])
    def test_or_not_specification(self, fruit, expected):
        specification = FruitIsSweet().or_not(FruitIsYellow())

        result = specification.is_satisfied_by(fruit)

        assert result is expected

    @pytest.mark.parametrize('fruit, expected', [
        (lemon, False),
        (orange, False),
        (apple, True),
    ])
    def test_not_specification(self, fruit, expected):
        specification = FruitIsSour().not_()

        result = specification.is_satisfied_by(fruit)

        assert result is expected

    @pytest.mark.parametrize('fruit, expected', [
        (lemon, False),
        (orange, True),
        (apple, False),
        (avocado, True),
    ])
    def test_chain_specification(self, fruit, expected):
        specification = FruitIsSour().and_not(
            FruitIsYellow()
        ).or_(
            FruitIsSour().not_().and_not(
                FruitIsSweet()
            )
        )

        result = specification.is_satisfied_by(fruit)

        assert result is expected


class TestSutoppuBitwiseSyntax:
    @pytest.mark.parametrize('fruit, expected', [
        (lemon, False),
        (orange, True),
        (apple, False),
    ])
    def test_and_specification(self, fruit, expected):
        specification = FruitIsSweet() & FruitIsSour()
        result = specification.is_satisfied_by(fruit)

        assert result is expected

    @pytest.mark.parametrize('fruit, expected', [
        (lemon, True),
        (orange, True),
        (avocado, False),
    ])
    def test_or_specification(self, fruit, expected):
        specification = FruitIsSweet() | FruitIsSour()

        result = specification.is_satisfied_by(fruit)

        assert result is expected

    @pytest.mark.parametrize('fruit, expected', [
        (lemon, False),
        (orange, False),
        (apple, True),
    ])
    def test_not_specification(self, fruit, expected):
        specification = ~ FruitIsSour()

        result = specification.is_satisfied_by(fruit)

        assert result is expected

    @pytest.mark.parametrize('fruit, expected', [
        (lemon, False),
        (orange, True),
        (apple, False),
        (avocado, True),
    ])
    def test_chain_specification(self, fruit, expected):
        specification = (FruitIsSour() & ~ FruitIsYellow()) \
            | (~ FruitIsSour() & ~ FruitIsSweet())

        result = specification.is_satisfied_by(fruit)

        assert result is expected
