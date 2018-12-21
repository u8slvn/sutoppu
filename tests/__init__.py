from sutoppu import Specification


class Fruit:
    def __init__(self, color, sweet, bitter):
        self.color = color
        self.sweet = sweet
        self.bitter = bitter


class FruitIsYellow(Specification):
    description = 'Fruit must be yellow.'

    def _is_satisfied_by(self, fruit):
        return fruit.color == 'yellow'


class FruitIsSweet(Specification):
    description = 'Fruit must be sweet.'

    def _is_satisfied_by(self, fruit):
        return fruit.sweet is True


class FruitIsBitter(Specification):
    description = 'Fruit must be bitter.'

    def _is_satisfied_by(self, fruit):
        return fruit.bitter is True
