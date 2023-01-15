from contracts import session_service
from game_model.commands.move_figure.command import MoveFigure
from game_model.commands.resign import Resign
from game_model.game.manager.command import Command
from game_model.game.model import Position
from services.session_service.domain.models import PlayerModel


def parse_command(player: PlayerModel, command: dict) -> Command:
    print('[Parser] Parsing command...')
    command_id = command.get('command_id')

    try:
        if command_id is None:
            raise session_service.ExecuteCommandError('Invalid format')

        if command_id == "turn.move":
            start = Position(*command["from"])
            end = Position(*command["to"])
            return MoveFigure(player=player.in_game, start=start, end=end)

        if command_id == "turn.resign":
            return Resign(player=player.in_game)

        print('[Parser] Raising "Unknown command"')
        raise session_service.ExecuteCommandError(f'Unknown command id {command_id!r}')
    except KeyError:
        print('[Parser] Raising "Invalid format"')
        raise session_service.ExecuteCommandError('Invalid format')
