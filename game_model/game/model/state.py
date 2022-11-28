from dataclasses import dataclass
from enum import Enum, auto
from game_model.game.model import Player, Board, Prison


class GameStatus(Enum):
    FIRST_PLAYER_TURN = auto()
    SECOND_PLAYER_TURN = auto()

    FIRST_PLAYER_WIN = auto()
    SECOND_PLAYER_WIN = auto()
    DRAW = auto()


@dataclass
class GameState:
    status: GameStatus

    first_player: Player
    second_player: Player

    board: Board

    first_player_prison: Prison
    second_player_prison: Prison
