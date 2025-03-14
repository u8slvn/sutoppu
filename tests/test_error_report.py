from __future__ import annotations

import pytest

from tests.conftest import FruitIsBitter
from tests.conftest import FruitIsSweet
from tests.conftest import avocado
from tests.conftest import lemon
from tests.conftest import orange


@pytest.mark.parametrize(
    "fruit, expected, failed",
    [
        (
            lemon,
            False,
            {
                "FruitIsSweet": "Fruit must be sweet.",
                "FruitIsBitter": "Expected condition to NOT satisfy: Fruit must be bitter.",
            },
        ),
        (
            orange,
            False,
            {
                "FruitIsBitter": "Expected condition to NOT satisfy: Fruit must be bitter."
            },
        ),
        (avocado, False, {"FruitIsSweet": "Fruit must be sweet."}),
    ],
)
def test_basic_report_specification(fruit, expected, failed):
    specification = FruitIsSweet() & ~FruitIsBitter()
    result = specification.is_satisfied_by(fruit)

    assert result is expected
    assert specification.errors == failed


def test_report_reset_after_two_uses():
    specification = FruitIsSweet() & ~FruitIsBitter()

    result = specification.is_satisfied_by(orange)

    expected_failed = {
        "FruitIsBitter": "Expected condition to NOT satisfy: Fruit must be bitter."
    }
    assert result is False
    assert specification.errors == expected_failed

    result = specification.is_satisfied_by(avocado)

    expected_failed = {"FruitIsSweet": "Fruit must be sweet."}
    assert result is False
    assert specification.errors == expected_failed
