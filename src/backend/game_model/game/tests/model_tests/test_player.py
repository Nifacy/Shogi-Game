import unittest
from copy import copy

from game_model.game.model import Player


class TestPlayer(unittest.TestCase):
    def test_init(self):
        try:
            Player()
        except ValueError:
            self.fail(f"Сигнатура класса {Player} не соответствует ожидаемой")

    def test_copy(self):
        original = Player()
        copied = copy(original)

        self.assertEqual(original, copied, f"Объекты класса {Player} должны быть идентичны после копирования")
