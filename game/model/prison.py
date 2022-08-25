from typing import Iterable, List

from game.model import Player
from game.model.figure import Figure


class Prison:
    _figures: List[Figure]
    _owner: Player

    def __init__(self, owner: Player):
        self._figures = []
        self._owner = owner

    def add_figure(self, figure: Figure):
        if figure not in self._figures:
            figure.owner = self._owner
            self._figures.append(figure)

    def remove_figure(self, figure: Figure):
        if figure in self._figures:
            self._figures.remove(figure)

    @property
    def figures(self) -> Iterable[Figure]:
        return tuple(self._figures)
