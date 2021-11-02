"""Sutoppu
A simple implementation of Specification pattern.

Copyright (C) 2019 - u8slvn - Sylvain Collas
This module is released under the MIT License:
http://www.opensource.org/licenses/mit-license.php
"""

from abc import ABCMeta, abstractmethod
import functools

__all__ = ["Specification"]
__version__ = "0.1.2"


class _SpecificationMeta(ABCMeta):
    """Add a little bit of magic, _SpecificationMeta automatically apply the
    class method '_report_errors' as decorator for the 'is_satisfied_by'
    method. It allows to simplify Specification declaration by declaring only
    'is_satisfied_by' without paying attention of the '_report_errors'
    decorator.
    """

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if hasattr(cls, "is_satisfied_by") and hasattr(cls, "_report_errors"):
            cls.is_satisfied_by = cls._report_errors(cls.is_satisfied_by)
        return cls


class Specification(metaclass=_SpecificationMeta):
    """Specification base class, each domain specification must inherit from
    this class.
    """

    description = "No description provided."

    def __init__(self):
        self.errors = {}

    @classmethod
    def _report_errors(cls, func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            self.errors = {}  # reset the errors dict
            result = func(self, *args, **kwargs)
            self._report_error(result)
            return result

        return wrapper

    @abstractmethod
    def is_satisfied_by(self, candidate: any) -> bool:
        raise NotImplementedError

    def _report_error(self, result: bool):
        """Each time a specification verification failed, this method
        report it in the 'errors' dict attribute.
        """
        if not result:
            self.errors.update({self.class_name: self.description})

    @property
    def class_name(self):
        return self.__class__.__name__

    def __and__(self, spec: "Specification") -> "_AndSpecification":
        return _AndSpecification(self, spec)

    def __or__(self, spec: "Specification") -> "_OrSpecification":
        return _OrSpecification(self, spec)

    def __invert__(self) -> "_NotSpecification":  # not
        return _NotSpecification(self)

    def __call__(self, candidate: any):
        """Extra syntax for more facilities."""
        return self.is_satisfied_by(candidate)

    def __repr__(self):
        return f"<{self.class_name}: {self.description}>"


class _AndOrSpecification(Specification):
    """Base class for 'And' and 'Or' specifications."""

    def __init__(self, spec_a: Specification, spec_b: Specification):
        super().__init__()
        self._specs = (spec_a, spec_b)

    def _report_error(self, _):
        """Gets the children spec errors and merge them into its own.
        The goal behind this it to propagate the errors through all the
        parents specifications.
        The result argument is useless in this case.
        """
        for spec in self._specs:
            self.errors = {**self.errors, **spec.errors}

    def is_satisfied_by(self, candidate: any) -> bool:
        results = (spec.is_satisfied_by(candidate) for spec in self._specs)

        return self._check(*results)

    @abstractmethod
    def _check(self, spec_a: bool, spec_b: bool):
        """Check the operator logic."""
        raise NotImplementedError


class _AndSpecification(_AndOrSpecification):
    def _check(self, spec_a: bool, spec_b: bool) -> bool:
        return spec_a and spec_b


class _OrSpecification(_AndOrSpecification):
    def _check(self, spec_a: bool, spec_b: bool) -> bool:
        return spec_a or spec_b


class _NotSpecification(Specification):
    def __init__(self, spec: Specification):
        super().__init__()
        self._spec = spec

    def _report_error(self, result: bool):
        """Due to its inversion logic the not specification must report
        an error if the checked specification did not failed.
        The description is prefixed with 'Not ~'  to indicate this.
        """
        if not result:
            description = f"Not ~ {self._spec.description}"
            self.errors.update({self._spec.class_name: description})

    def is_satisfied_by(self, candidate: any) -> bool:
        result = self._spec.is_satisfied_by(candidate)

        return not result
