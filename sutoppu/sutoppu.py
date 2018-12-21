#!/usr/bin/env python3
# coding: utf-8

from abc import ABC, abstractmethod


class AbstractSpecification(ABC):
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
    description = 'This must check something.'

    def __init__(self):
        self.failed = dict()

    def is_satisfied_by(self, candidate):
        self.failed = dict()
        result = self._is_satisfied_by(candidate)
        self._report_error(result)

        return result

    @abstractmethod
    def _is_satisfied_by(self, candidate):
        raise NotImplementedError

    def _report_error(self, result):
        if not result:
            class_name = self.__class__.__name__
            self.failed[class_name] = self.get_description()

    @classmethod
    def get_description(cls):
        return cls.description

    def and_(self, spec):
        return _AndSpecification(self, spec)

    def and_not(self, spec):
        return _AndNotSpecification(self, spec)

    def or_(self, spec):
        return _OrSpecification(self, spec)

    def or_not(self, spec):
        return _OrNotSpecification(self, spec)

    def not_(spec):
        return _NotSpecification(spec)

    # Bitwise operators overloading for a shorter syntax

    def __and__(self, spec):
        return self.and_(spec)

    def __or__(self, spec):
        return self.or_(spec)

    def __invert__(self):
        return self.not_()


class OperatorSpecification(Specification):
    def __init__(self, *specifications):
        super().__init__()
        self._specs = list(specifications)
        assert 1 <= len(self._specs) <= 2, \
            'OperatorSpecification classes should be instantiated with '\
            'at minimum one parameter, and maximum two.'

    def _report_error(self, result):
        for spec in self._specs:
            self.failed = {**self.failed, **spec.failed}

    def _is_satisfied_by(self, candidate):
        results = [spec.is_satisfied_by(candidate) for spec in self._specs]

        return self._check(*results)

    @abstractmethod
    def _check(self, candidate):
        raise NotImplementedError


class _AndSpecification(OperatorSpecification):
    def _check(self, spec_a, spec_b):
        return spec_a and spec_b


class _AndNotSpecification(OperatorSpecification):
    def _check(self, spec_a, spec_b):
        return spec_a and not spec_b


class _OrSpecification(OperatorSpecification):
    def _check(self, spec_a, spec_b):
        return spec_a or spec_b


class _OrNotSpecification(OperatorSpecification):
    def _check(self, spec_a, spec_b):
        return spec_a or not spec_b


class _NotSpecification(OperatorSpecification):
    def _report_error(self, result):
        if not result and isinstance(self._specs[0], Specification):
            class_name = f"Not{self._specs[0].__class__.__name__}"
            description = f"Not ~ {self._specs[0].get_description()}"
            self.failed[class_name] = description

    def _check(self, spec):
        return not spec
