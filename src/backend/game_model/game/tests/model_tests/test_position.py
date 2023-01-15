import unittest

from game_model.game.model import Position


class TestPosition(unittest.TestCase):
    def test_init(self):
        try:
            Position(x=3, y=3)
        except:
            self.fail(f"Сигнатура конструктора класса {Position} не соответствует ожидаемой")

    def test_keys(self):
        pos = Position(x=3, y=3)

        self.assertTrue(hasattr(pos, "x"), f"Объект класса {Position} должен содержать поле 'x'")
        self.assertTrue(hasattr(pos, "y"), f"Объект класса {Position} должен содержать поле 'y'")
