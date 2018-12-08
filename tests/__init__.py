from sutoppu import AbstractSpecification


class Fruit:
    def __init__(self, color, sweet, sour):
        self.color = color
        self.sweet = sweet
        self.sour = sour


class FruitIsYellow(AbstractSpecification):
    def is_satisfied_by(self, fruit) -> bool:
        return fruit.color == 'yellow'


class FruitIsSweet(AbstractSpecification):
    def is_satisfied_by(self, fruit) -> bool:
        return fruit.sweet is True


class FruitIsSour(AbstractSpecification):
    def is_satisfied_by(self, fruit) -> bool:
        return fruit.sour is True
