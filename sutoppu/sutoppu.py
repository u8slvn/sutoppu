#!/usr/bin/env python3
# coding: utf-8

from abc import ABC, abstractmethod


class AbstractSpecification(ABC):
    @abstractmethod
    def is_satisfied_by(self, candidate) -> bool:
        pass

    @abstractmethod
    def and_(self, specification):
        pass

    @abstractmethod
    def or_(self, specification):
        pass

    @abstractmethod
    def not_(self):
        pass


class Specification(AbstractSpecification):
    @abstractmethod
    def is_satisfied_by(self, candidate) -> bool:
        pass

    def and_(self, spec: AbstractSpecification) -> AbstractSpecification:
        return AndSpecification(self, spec)

    def or_(self, spec: AbstractSpecification) -> AbstractSpecification:
        return OrSpecification(self, spec)

    def not_(self) -> AbstractSpecification:
        return NotSpecification(self)


class AndSpecification(Specification):
    def __init__(self, spec_a: Specification, spec_b: Specification):
        self._spec_a = spec_a
        self._spec_b = spec_b

    def is_satisfied_by(self, candidate) -> bool:
        return self._spec_a.is_satisfied_by(candidate) \
            and self._spec_b.is_satisfied_by(candidate)


class OrSpecification(Specification):
    def __init__(self, spec_a: Specification, spec_b: Specification):
        self._spec_a = spec_a
        self._spec_b = spec_b

    def is_satisfied_by(self, candidate) -> bool:
        return self._spec_a.is_satisfied_by(candidate) \
            or self._spec_b.is_satisfied_by(candidate)


class NotSpecification(Specification):
    def __init__(self, spec: Specification):
        self._spec = spec

    def is_satisfied_by(self, candidate) -> bool:
        return not self._spec.is_satisfied_by(candidate)
