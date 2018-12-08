from sutoppu import Specification


class Fruit:
    def __init__(self, color, sweet, sour):
        self.color = color
        self.sweet = sweet
        self.sour = sour


class FruitIsYellow(Specification):
    def is_satisfied_by(self, fruit) -> bool:
        return fruit.color == 'yellow'


class FruitIsSweet(Specification):
    def is_satisfied_by(self, fruit) -> bool:
        return fruit.sweet is True


class FruitIsSour(Specification):
    def is_satisfied_by(self, fruit) -> bool:
        return fruit.sour is True
