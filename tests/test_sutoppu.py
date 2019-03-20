#!/usr/bin/env python3
# coding: utf-8

import pytest

from tests import Fruit, FruitIsSweet, FruitIsBitter, FruitIsYellow

lemon = Fruit(color='yellow', sweet=False, bitter=True)
orange = Fruit(color='orange', sweet=True, bitter=True)
apple = Fruit(color='red', sweet=True, bitter=False)
avocado = Fruit(color='green', sweet=False, bitter=False)


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
        specification = FruitIsSweet().and_(FruitIsBitter())
        result = specification.is_satisfied_by(fruit)

        assert result is expected

    @pytest.mark.parametrize('fruit, expected', [
        (lemon, False),
        (orange, False),
        (apple, True),
    ])
    def test_and_not_specification(self, fruit, expected):
        specification = FruitIsSweet().and_not(FruitIsBitter())
        result = specification.is_satisfied_by(fruit)

        assert result is expected

    @pytest.mark.parametrize('fruit, expected', [
        (lemon, True),
        (orange, True),
        (avocado, False),
    ])
    def test_or_specification(self, fruit, expected):
        specification = FruitIsSweet().or_(FruitIsBitter())

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
        specification = FruitIsBitter().not_()

        result = specification.is_satisfied_by(fruit)

        assert result is expected

    @pytest.mark.parametrize('fruit, expected', [
        (lemon, False),
        (orange, True),
        (apple, False),
        (avocado, True),
    ])
    def test_chain_specification(self, fruit, expected):
        specification = FruitIsBitter().and_not(
            FruitIsYellow()
        ).or_(
            FruitIsBitter().not_().and_not(
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
        specification = FruitIsSweet() & FruitIsBitter()
        result = specification.is_satisfied_by(fruit)

        assert result is expected

    @pytest.mark.parametrize('fruit, expected', [
        (lemon, True),
        (orange, True),
        (avocado, False),
    ])
    def test_or_specification(self, fruit, expected):
        specification = FruitIsSweet() | FruitIsBitter()

        result = specification.is_satisfied_by(fruit)

        assert result is expected

    @pytest.mark.parametrize('fruit, expected', [
        (lemon, False),
        (orange, False),
        (apple, True),
    ])
    def test_not_specification(self, fruit, expected):
        specification = ~ FruitIsBitter()

        result = specification.is_satisfied_by(fruit)

        assert result is expected

    @pytest.mark.parametrize('fruit, expected', [
        (lemon, False),
        (orange, True),
        (apple, False),
        (avocado, True),
    ])
    def test_chain_specification(self, fruit, expected):
        specification = (FruitIsBitter() & ~ FruitIsYellow()) \
            | (~ FruitIsBitter() & ~ FruitIsSweet())

        result = specification.is_satisfied_by(fruit)

        assert result is expected


class TestSutoppuFailureReport:
    @pytest.mark.parametrize('fruit, expected, failed', [
        (lemon, False, {'FruitIsSweet': 'Fruit must be sweet.',
                        'FruitIsBitter': 'Not ~ Fruit must be bitter.'}),
        (orange, False, {'FruitIsBitter': 'Not ~ Fruit must be bitter.'}),
        (avocado, False, {'FruitIsSweet': 'Fruit must be sweet.'}),
    ])
    def test_basic_report_specification(self, fruit, expected, failed):
        specification = FruitIsSweet().and_(FruitIsBitter().not_())
        result = specification.is_satisfied_by(fruit)

        assert result is expected
        assert specification.errors == failed

    def test_report_reset_after_two_uses(self):
        specification = FruitIsSweet().and_(FruitIsBitter().not_())

        result = specification.is_satisfied_by(orange)

        expected_failed = {'FruitIsBitter': 'Not ~ Fruit must be bitter.'}
        assert result is False
        assert specification.errors == expected_failed

        result = specification.is_satisfied_by(avocado)

        expected_failed = {'FruitIsSweet': 'Fruit must be sweet.'}
        assert result is False
        assert specification.errors == expected_failed
