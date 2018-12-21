from sutoppu import Specification


class Fruit:
    def __init__(self, color, sweet, sour):
        self.color = color
        self.sweet = sweet
        self.sour = sour


class FruitIsYellow(Specification):
    description = 'Fruit must be yellow.'

    def _is_satisfied_by(self, fruit):
        return fruit.color == 'yellow'


class FruitIsSweet(Specification):
    description = 'Fruit must be sweet.'

    def _is_satisfied_by(self, fruit):
        return fruit.sweet is True


class FruitIsSour(Specification):
    description = 'Fruit must be sour.'

    def _is_satisfied_by(self, fruit):
        return fruit.sour is True
