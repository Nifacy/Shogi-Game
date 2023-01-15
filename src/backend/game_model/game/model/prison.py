from typing import Iterable, List

from game_model.game.model import Player
from game_model.game.model.figure import Figure


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

    @classmethod
    def equals(cls, first: "Prison", second: "Prison") -> bool:
        return (first._owner, first._figures) == (second._owner, second._figures)

    def __eq__(self, other: "Prison") -> bool:
        return Prison.equals(self, other)
