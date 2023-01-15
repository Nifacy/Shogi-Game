from enum import Enum

from game_model.game.model import Position


class MoveDirection(Enum):
    UP = Position(x=0, y=1)
    DOWN = Position(x=0, y=-1)

    LEFT = Position(x=-1, y=0)
    RIGHT = Position(x=1, y=0)

    UP_LEFT = Position(x=-1, y=1)
    UP_RIGHT = Position(x=1, y=1)

    DOWN_LEFT = Position(x=-1, y=-1)
    DOWN_RIGHT = Position(x=1, y=-1)
