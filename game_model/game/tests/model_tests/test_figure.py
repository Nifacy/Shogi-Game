import unittest
from copy import copy

from game_model.game.model import Player, Figure
from game_model.game.tests.model_tests.plugs import FigurePlug


class TestFigure(unittest.TestCase):
    def test_init(self):
        try:
            FigurePlug(owner=Player())
        except ValueError:
            self.fail(f"Сигнатура конструктора класса {Figure} не соответствует ожидаемой")

    def test_copy(self):
        original = FigurePlug(owner=Player())
        copied = copy(original)

        self.assertEqual(original, copied, f"Объекты класса {Figure} должны быть идентичны после копирования")

    def test_owner(self):
        owner, other_owner = Player(), Player()
        figure = FigurePlug(owner=owner)

        self.assertEqual(owner, figure.owner, f"Поле 'owner' не содержит объект, переданный при инициализации")

        figure.owner = other_owner

        self.assertEqual(other_owner, figure.owner, f"Поле 'owner' не меняет владельца фигуры")
