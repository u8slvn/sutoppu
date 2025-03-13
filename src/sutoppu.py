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

    This metaclass automatically decorates the 'is_satisfied_by' method with
    the '_report_errors' decorator, removing the need for manual decoration.

    This simplifies the implementation of concrete Specification classes by allowing
    developers to focus solely on the business rule logic in 'is_satisfied_by' without
    worrying about error reporting.
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
    """Base class for implementing domain-specific business rules as specifications.

    The Specification pattern allows business rules to be defined as objects that can:
    - Evaluate if an object satisfies a specific rule
    - Combine with other specifications using logical operators (&, |, ~)
    - Report detailed errors when rules are not satisfied

    To implement a specification:
    1. Subclass Specification[T] with appropriate type parameter
    2. Provide a descriptive 'description' class attribute
    3. Implement the 'is_satisfied_by' method with your business logic

    Attributes:
        description (str): Human-readable description of the rule
        errors (dict): Contains error messages after validation fails
    """

    description = "No description provided."

    def __init__(self) -> None:
        self.errors: dict[str, str] = {}

    @classmethod
    def _report_errors(
        cls, func: Callable[[Self, T], bool]
    ) -> Callable[[Self, T], bool]:
        """Decorator for error reporting.

        Wraps the 'is_satisfied_by' method to handle error reporting automatically.
        When validation fails, it registers the error in the 'errors' dictionary.

        Args:
            func: The 'is_satisfied_by' method to wrap

        Returns:
            Wrapped function with error reporting capability
        """

        @functools.wraps(func)
        def wrapper(self: Self, candidate: T) -> bool:
            self.errors = {}  # reset the errors dict
            result = func(self, candidate)
            self._report_error(result)
            return result

        return wrapper

    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        """Evaluate whether the candidate satisfies this specification.

        This is where the actual business logic should be implemented in subclasses.

        Args:
            candidate: The object to validate against this specification

        Returns:
            True if the candidate satisfies the specification, False otherwise
        """
        raise NotImplementedError

    def _report_error(self, result: bool) -> None:
        """Register an error message when validation fails.

        When a specification validation fails (result is False), this method
        records the error in the 'errors' dictionary attribute.

        Args:
            result: Result of the validation
        """
        if result is False:
            self.errors.update({self.class_name: self.description})

    @property
    def class_name(self) -> str:
        """Get the class name of this specification.

        Returns:
            Name of the specification class
        """
        return self.__class__.__name__

    def __and__(self, spec: Specification[T]) -> _AndSpecification[T]:
        """Combine this specification with another using logical AND.

        Args:
            spec: Another specification to combine with

        Returns:
            A new specification that is satisfied only when both specifications are satisfied
        """
        return _AndSpecification(self, spec)

    def __or__(self, spec: Specification[T]) -> _OrSpecification[T]:
        """Combine this specification with another using logical OR.

        Args:
            spec: Another specification to combine with

        Returns:
            A new specification that is satisfied when either specification is satisfied
        """
        return _OrSpecification(self, spec)

    def __invert__(self) -> _NotSpecification[T]:
        """Negate this specification using logical NOT.

        Returns:
            A new specification that is satisfied when this specification is not satisfied
        """
        return _NotSpecification(self)

    def __call__(self, candidate: Any) -> bool:
        """Alternative syntax for checking if a candidate satisfies this specification.

        Allows specifications to be used as callable objects.

        Args:
            candidate: The object to validate

        Returns:
            True if the candidate satisfies the specification, False otherwise
        """
        return self.is_satisfied_by(candidate)

    def __repr__(self) -> str:
        """Get a string representation of this specification.

        Returns:
            String representation including class name and description
        """
        return f"<{self.class_name}: {self.description}>"


class _AndOrSpecification(Specification[T]):
    """Base class for composite specifications using AND/OR logic.

    This abstract base class provides common functionality for both
    AND and OR composite specifications.

    Attributes:
        _specs: Tuple containing the two specifications being combined
    """

    def __init__(self, spec_a: Specification[T], spec_b: Specification[T]) -> None:
        super().__init__()
        self._specs = (spec_a, spec_b)

    def _report_error(self, _: bool) -> None:
        """Collect and propagate errors from child specifications.

        This method merges errors from child specifications into this
        composite specification's errors dictionary.

        The result parameter is ignored since errors are collected directly
        from child specifications.
        """
        for spec in self._specs:
            self.errors.update(spec.errors)

    def is_satisfied_by(self, candidate: T) -> bool:
        """Evaluate the candidate against both child specifications.

        Args:
            candidate: Object to validate

        Returns:
            Result of applying the logical operation to both child results
        """
        results = (spec.is_satisfied_by(candidate) for spec in self._specs)

        return self._check(*results)

    @abstractmethod
    def _check(self, spec_a: bool, spec_b: bool) -> bool:
        """Apply the specific logical operation to the results.

        This abstract method is implemented by subclasses to provide
        the specific boolean logic (AND or OR).

        Args:
            spec_a: Result from the first specification
            spec_b: Result from the second specification

        Returns:
            Combined result based on the logical operation
        """
        raise NotImplementedError


class _AndSpecification(_AndOrSpecification[T]):
    """Composite specification using logical AND.

    A candidate satisfies this specification only if it satisfies
    both of the component specifications.
    """

    def _check(self, spec_a: bool, spec_b: bool) -> bool:
        """Apply logical AND to the validation results.

        Args:
            spec_a: Result from the first specification
            spec_b: Result from the second specification

        Returns:
            True only if both results are True
        """
        return spec_a and spec_b


class _OrSpecification(_AndOrSpecification[T]):
    """Composite specification using logical OR.

    A candidate satisfies this specification if it satisfies
    either of the component specifications.
    """

    def _check(self, spec_a: bool, spec_b: bool) -> bool:
        """Apply logical OR to the validation results.

        Args:
            spec_a: Result from the first specification
            spec_b: Result from the second specification

        Returns:
            True if either result is True
        """
        return spec_a or spec_b


class _NotSpecification(Specification[T]):
    """Composite specification using logical NOT.

    A candidate satisfies this specification if it does not satisfy
    the component specification.
    """

    description_format = "Expected condition to NOT satisfy: {0}"

    def __init__(self, spec: Specification[T]) -> None:
        super().__init__()
        self._spec = spec
        self.description = self.description_format.format(self._spec.description)

    def _report_error(self, result: bool) -> None:
        """Report errors for the negated specification.

        Due to the negation logic, an error is reported when the inner
        specification passes validation.

        Args:
            result: Result of the negated validation
        """
        if result is False:
            self.errors.update({self._spec.class_name: self.description})

    def is_satisfied_by(self, candidate: T) -> bool:
        """Evaluate the candidate with negated logic.

        Args:
            candidate: Object to validate

        Returns:
            True if the inner specification returns False, and vice versa
        """
        result = self._spec.is_satisfied_by(candidate)

        return not result
