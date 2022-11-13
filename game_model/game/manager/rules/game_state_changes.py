from typing import NamedTuple

from game_model.game.model import GameState


class GameStateChanges(NamedTuple):
    old_state: GameState
    new_state: GameState
