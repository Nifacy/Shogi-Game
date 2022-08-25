from typing import Union

from game.model.figure import Figure


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
