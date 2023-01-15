from itertools import product
from typing import Tuple, Dict

from game_model.game.model.cell import Cell
from game_model.game.model.position import Position


class UnavailablePosition(Exception):
    _position: Position
    _msg_template = "Unavailable to get cell by position {pos}"

    def __init__(self, pos: Position):
        super().__init__(self._msg_template.format(pos=pos))
        self._position = pos

    @property
    def position(self) -> Position:
        return self._position


BoardSize = Tuple[int, int]


class Board:
    _cells: Dict[Position, Cell]
    _size: BoardSize

    def __init__(self, size: BoardSize):
        self._size = size
        self._cells = {pos: Cell() for pos in product(*map(range, size))}

    @property
    def size(self) -> BoardSize:
        return self._size

    def get_cell(self, pos: Position) -> Cell:
        w, h = self.size

        if not(0 <= pos.x < w) or not(0 <= pos.y < h):
            raise UnavailablePosition(pos)

        return self._cells[pos]

    @classmethod
    def equals(cls, first: "Board", second: "Board") -> bool:
        if first.size != second.size:
            return False

        for pos in product(*map(range, first.size)):
            first_figure = second.get_cell(Position(*pos)).get_figure()
            second_figure = first.get_cell(Position(*pos)).get_figure()

            if first_figure is None or second_figure is None:
                return False

            if first_figure != second_figure:
                return False

        return True

    def __eq__(self, other: "Board") -> bool:
        return Board.equals(self, other)
