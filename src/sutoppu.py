"""Sutoppu
A simple implementation of Specification pattern.

Copyright (C) 2018 - u8slvn - Sylvain Collas
This module is released under the MIT License:
https://www.opensource.org/licenses/mit-license.php
"""
from __future__ import annotations

import functools
import sys

from abc import ABCMeta
from abc import abstractmethod
from importlib import metadata
from typing import Any
from typing import Callable
from typing import Generic
from typing import TypeVar


if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


__all__ = ["Specification"]
__version__ = metadata.version("sutoppu")


class _SpecificationMeta(ABCMeta):
    """Specification metaclass

    Add a little bit of magic, _SpecificationMeta automatically apply the
    class method '_report_errors' as decorator for the 'is_satisfied_by'
    method. It allows to simplify Specification declaration by declaring only
    'is_satisfied_by' without paying attention of the '_report_errors'
    decorator.
    """

    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
    ) -> _SpecificationMeta:
        class_ = super().__new__(cls, name, bases, namespace)
        if hasattr(class_, "is_satisfied_by") and hasattr(class_, "_report_errors"):
            class_.is_satisfied_by = class_._report_errors(class_.is_satisfied_by)
        return class_


T = TypeVar("T")


class Specification(Generic[T], metaclass=_SpecificationMeta):
    """Specification base class

    Each domain specification must inherit from this class.
    """

    description = "No description provided."

    def __init__(self) -> None:
        self.errors: dict[str, str] = {}

    @classmethod
    def _report_errors(
        cls, func: Callable[[Self, T], bool]
    ) -> Callable[[Self, T], bool]:
        @functools.wraps(func)
        def wrapper(self: Self, candidate: T) -> bool:
            self.errors = {}  # reset the errors dict
            result = func(self, candidate)
            self._report_error(result)
            return result

        return wrapper

    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        raise NotImplementedError

    def _report_error(self, result: bool) -> None:
        """Each time a specification verification failed, this method
        report it in the 'errors' dict attribute.
        """
        if result is False:
            self.errors.update({self.class_name: self.description})

    @property
    def class_name(self) -> str:
        return self.__class__.__name__

    def __and__(self, spec: Specification[T]) -> _AndSpecification[T]:
        return _AndSpecification(self, spec)

    def __or__(self, spec: Specification[T]) -> _OrSpecification[T]:
        return _OrSpecification(self, spec)

    def __invert__(self) -> _NotSpecification[T]:  # not
        return _NotSpecification(self)

    def __call__(self, candidate: Any) -> bool:
        """Additional syntax for ease of use."""
        return self.is_satisfied_by(candidate)

    def __repr__(self) -> str:
        return f"<{self.class_name}: {self.description}>"


class _AndOrSpecification(Specification[T]):
    """Base class for 'And' and 'Or' specifications."""

    def __init__(self, spec_a: Specification[T], spec_b: Specification[T]) -> None:
        super().__init__()
        self._specs = (spec_a, spec_b)

    def _report_error(self, _: bool) -> None:
        """Gets the children spec errors and merge them into its own.
        Allows to propagate errors through all parents specifications.
        The result parameter is ignored in this case.
        """
        for spec in self._specs:
            self.errors.update(spec.errors)

    def is_satisfied_by(self, candidate: T) -> bool:
        results = (spec.is_satisfied_by(candidate) for spec in self._specs)

        return self._check(*results)

    @abstractmethod
    def _check(self, spec_a: bool, spec_b: bool) -> bool:
        """Check the operator logic."""
        raise NotImplementedError


class _AndSpecification(_AndOrSpecification[T]):
    def _check(self, spec_a: bool, spec_b: bool) -> bool:
        return spec_a and spec_b


class _OrSpecification(_AndOrSpecification[T]):
    def _check(self, spec_a: bool, spec_b: bool) -> bool:
        return spec_a or spec_b


class _NotSpecification(Specification[T]):
    def __init__(self, spec: Specification[T]) -> None:
        super().__init__()
        self._spec = spec

    def _report_error(self, result: bool) -> None:
        """Due to its inversion logic the not specification must report
        an error if the checked specification did not fail.
        The description is prefixed with 'Not ~'  to indicate this.
        """
        if not result:
            description = f"Not ~ {self._spec.description}"
            self.errors.update({self._spec.class_name: description})

    def is_satisfied_by(self, candidate: T) -> bool:
        result = self._spec.is_satisfied_by(candidate)

        return not result
