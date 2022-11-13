from enum import Enum, auto
from typing import NamedTuple

from game_model.game.model import Player, Board, Prison


class GameStatus(Enum):
    FIRST_PLAYER_TURN = auto()
    SECOND_PLAYER_TURN = auto()

    FIRST_PLAYER_WIN = auto()
    SECOND_PLAYER_WIN = auto()
    DRAW = auto()


class GameState(NamedTuple):
    status: GameStatus

    first_player: Player
    second_player: Player

    board: Board

    first_player_prison: Prison
    second_player_prison: Prison
