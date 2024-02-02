from __future__ import annotations

from sutoppu import Specification


class Fruit:
    def __init__(self, color, sweet, bitter):
        self.color = color
        self.sweet = sweet
        self.bitter = bitter


class FruitIsYellow(Specification):
    description = "Fruit must be yellow."

    def is_satisfied_by(self, fruit):
        return fruit.color == "yellow"


class FruitIsSweet(Specification):
    description = "Fruit must be sweet."

    def is_satisfied_by(self, fruit):
        return fruit.sweet is True


class FruitIsBitter(Specification):
    description = "Fruit must be bitter."

    def is_satisfied_by(self, fruit):
        return fruit.bitter is True


lemon = Fruit(color="yellow", sweet=False, bitter=True)
orange = Fruit(color="orange", sweet=True, bitter=True)
apple = Fruit(color="red", sweet=True, bitter=False)
avocado = Fruit(color="green", sweet=False, bitter=False)
