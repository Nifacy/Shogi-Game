from typing import Union

from game_model.game.model.figure import Figure


class Cell:
    _figure: Union[Figure, None]

    def __init__(self):
        self._figure = None

    def get_figure(self) -> Union[Figure, None]:
        return self._figure

    def put_figure(self, figure: Figure):
        self._figure = figure

    def remove_figure(self):
        self._figure = None

    def is_empty(self) -> bool:
        return self.get_figure() is None

    @classmethod
    def equals(cls, first: "Cell", second: "Cell") -> bool:
        return first.get_figure() == second.get_figure()

    def __eq__(self, other: "Cell") -> bool:
        return Cell.equals(self, other)
