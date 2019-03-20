#!/usr/bin/env python3
# coding: utf-8

"""Sutoppu

A simple implementation of Specification pattern.

Copyright (C) 2019 - u8slvn - Sylvain Collas
This package is released under the MIT License:
http://www.opensource.org/licenses/mit-license.php

"""

from abc import ABC, abstractmethod

__all__ = ['Specification']


class AbstractSpecification(ABC):
    """Abstract specification interface
    Each specification class must implement this interface.
    """

    @abstractmethod
    def is_satisfied_by(self, candidate):
        raise NotImplementedError

    @abstractmethod
    def and_(self, specification):
        raise NotImplementedError

    @abstractmethod
    def and_not(self, specification):
        raise NotImplementedError

    @abstractmethod
    def or_(self, specification):
        raise NotImplementedError

    @abstractmethod
    def or_not(self, specification):
        raise NotImplementedError

    @abstractmethod
    def not_(self):
        raise NotImplementedError


class Specification(AbstractSpecification):
    """Specification base class
    Each domain specification must inherit from this class.
    """
    description = 'This must check something.'

    def __init__(self):
        self.errors = {}

    def is_satisfied_by(self, candidate: any):
        """The front `is satisfied by` method
        This method must never be overwrite. This is the entrypoint of
        the specification providing the error report mechanisme.
        """
        self.errors = {}  # reset the errors dict
        result = self._is_satisfied_by(candidate)
        self._report_error(result)

        return result

    @abstractmethod
    def _is_satisfied_by(self, candidate):
        """The back `is satisfied by` method
        It is where we write the custom domain rule by overriding this
        method.
        """
        raise NotImplementedError

    def _report_error(self, result: bool):
        """Error reporting method
        Each time a specification verification failed, this method
        report it in the `errors` dict attribute.
        """
        if not result:
            self.errors.update({self.class_name: self.description})

    @property
    def class_name(self):
        return self.__class__.__name__

    def and_(self, spec: 'Specification') -> '_AndSpecification':
        return _AndSpecification(self, spec)

    def and_not(self, spec: 'Specification') -> '_AndSpecification':
        return _AndSpecification(self, spec.not_())

    def or_(self, spec: 'Specification') -> '_OrSpecification':
        return _OrSpecification(self, spec)

    def or_not(self, spec: 'Specification') -> '_OrSpecification':
        return _OrSpecification(self, spec.not_())

    def not_(self) -> '_NotSpecification':
        return _NotSpecification(self)

    # Bitwise operators overloading for a shorter syntax

    def __and__(self, spec: 'Specification') -> '_AndSpecification':
        return self.and_(spec)

    def __or__(self, spec: 'Specification') -> '_OrSpecification':
        return self.or_(spec)

    def __invert__(self) -> '_NotSpecification':  # not
        return self.not_()


class AndOrSpecification(Specification):
    """Operator specification
    Base class for `And` and `Or` specifications.
    """

    def __init__(self, spec_a: Specification, spec_b: Specification):
        super().__init__()
        self._specs = (spec_a, spec_b)

    def _report_error(self, _):
        """And & Or report error
        Gets the children spec errors and merge them into its own.
        The goal behind this it to propagate the errors through all the
        parents specifications.
        The result param is useless in this case.
        """
        for spec in self._specs:
            self.errors = {**self.errors, **spec.errors}

    def _is_satisfied_by(self, candidate: any) -> bool:
        results = (spec.is_satisfied_by(candidate) for spec in self._specs)

        return self._check(*results)

    @abstractmethod
    def _check(self, spec_a, spec_b):
        """Check the operator logic."""
        raise NotImplementedError


class _AndSpecification(AndOrSpecification):
    def _check(self, spec_a: bool, spec_b: bool) -> bool:
        return spec_a and spec_b


class _OrSpecification(AndOrSpecification):
    def _check(self, spec_a: bool, spec_b: bool) -> bool:
        return spec_a or spec_b


class _NotSpecification(Specification):
    def __init__(self, spec: Specification):
        super().__init__()
        self._spec = spec

    def _report_error(self, result: bool):
        """Not specification report error
        Due to its inversion logic the not specification must report
        an error if the checked specification did not failed.
        The description is prefixed with `Not ~`  to indicate this.
        """
        if not result:
            description = f"Not ~ {self._spec.description}"
            self.errors.update({self._spec.class_name: description})

    def _is_satisfied_by(self, candidate: any) -> bool:
        result = self._spec.is_satisfied_by(candidate)

        return not result
