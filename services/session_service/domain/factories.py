from game_model.figures import Lion, Elephant, Giraffe, Chicken
from game_model.game.manager import GameManager
from game_model.game.model import GameState, Player, Board, Position, GameStatus, Prison


def state_factory(first_player: Player, second_player: Player) -> GameState:
    board = Board(size=(3, 5))

    board.get_cell(Position(0, 0)).put_figure(Elephant(owner=first_player))
    board.get_cell(Position(1, 0)).put_figure(Lion(owner=first_player))
    board.get_cell(Position(2, 0)).put_figure(Giraffe(owner=first_player))
    board.get_cell(Position(1, 1)).put_figure(Chicken(owner=first_player))

    board.get_cell(Position(2, 4)).put_figure(Elephant(owner=second_player))
    board.get_cell(Position(1, 4)).put_figure(Lion(owner=second_player))
    board.get_cell(Position(0, 4)).put_figure(Giraffe(owner=second_player))
    board.get_cell(Position(1, 3)).put_figure(Chicken(owner=second_player))

    return GameState(
        first_player=first_player, second_player=second_player,
        status=GameStatus.FIRST_PLAYER_TURN,
        board=board,
        first_player_prison=Prison(owner=first_player),
        second_player_prison=Prison(owner=second_player)
    )


def manager_factory(start_state: GameState) -> GameManager:
    manager = GameManager(start_state=start_state)
    return manager
