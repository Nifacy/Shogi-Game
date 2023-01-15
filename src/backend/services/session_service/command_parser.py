
from contracts import session_service
from game_model.commands.move_figure.command import MoveFigure
from game_model.commands.resign import Resign
from game_model.game.manager.command import Command
from game_model.game.model import Position
from services.session_service.domain.models import PlayerModel


def parse_command(player: PlayerModel, command: dict) -> Command:
    try:
        command_id = command["command_id"]

        if command_id == "turn.move":
            start = Position(*command["from"])
            end = Position(*command["to"])
            return MoveFigure(player=player, start=start, end=end)

        if command_id == "turn.resign":
            return Resign(player=player)
    except:
        raise session_service.ExecuteCommandError(description='Invalid format')
