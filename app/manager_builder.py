from game_model.game.manager import GameManager
from game_model.game.model import GameState


def build_manager(start_state: GameState) -> GameManager:
    manager = GameManager(start_state=start_state)
    return manager
