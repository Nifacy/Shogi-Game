import unittest

from game_model.game.model import Cell, Player
from game_model.game.tests.model_tests.plugs import FigurePlug


class TestCell(unittest.TestCase):
    def test_init(self):
        try:
            Cell()
        except:
            self.fail(f"Сигнатура конструктора класса {Cell} не соответствует ожидаемой")

    def test_methods(self):
        self.assertTrue(hasattr(Cell, "get_figure"), f"Класс {Cell} должен содержать метод 'get_figure'")
        self.assertTrue(hasattr(Cell, "put_figure"), f"Класс {Cell} должен содержать метод 'put_figure'")
        self.assertTrue(hasattr(Cell, "is_empty"),   f"Класс {Cell} должен содержать метод 'is_empty'")
        self.assertTrue(hasattr(Cell, "remove_figure"), f"Класс {Cell} должен содержать метод 'remove_figure'")

    def test_figure_state(self):
        cell = Cell()
        figure = FigurePlug(Player())

        self.assertTrue(cell.is_empty(), f"Объект класса {Cell} должен быть пустым по умолчанию")

        cell.put_figure(figure)

        self.assertFalse(cell.is_empty(), f"Объект класса {Cell} не должен быть пустым после того, как на него "
                                         f"поставили фигуру")
        self.assertEqual(figure, cell.get_figure(), f"Объект класса {Cell} должен возвращать фигуру, которую положили "
                                                    f"на нее")
