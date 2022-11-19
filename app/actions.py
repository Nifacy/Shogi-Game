from typing import Optional

from ddd_domain_events import DomainEvents

from app.events import CommandExecuteException
from app.manager_builder import build_manager
from app.models import User, Room
from game_model.commands.move_figure.command import MoveFigure
from game_model.game.manager.command import Command
from game_model.game.manager.exceptions import ExecuteCommandException
from game_model.game.model import Player, Position


async def authenticate_user(username: str, password: str) -> Optional[User]:
    user = await User.get(username=username)

    if not user:
        return None

    if not user.verify_password(password):
        return None

    return user


def get_command(room_id: int, player: Player, command: dict) -> Command:
    message_id = command["message_id"]

    if message_id == "turn.move":
        start = Position(*command["from"])
        end = Position(*command["to"])
        return MoveFigure(player=player, start=start, end=end)

    DomainEvents.raise_event(CommandExecuteException.EXECUTE_ERROR, detail="unknown command", player_id=player.id, room_id=room_id)


def raise_command_exception(room_id: int, exception: ExecuteCommandException):
    DomainEvents.raise_event(CommandExecuteException.EXECUTE_ERROR, detail=str(exception), player_id=exception.player.id, room_id=room_id)


async def send_command(room_id: int, user_id: int, command: dict):
    command = get_command(room_id, Player(id=user_id), command)
    if command is None: return

    print("PARSED COMMAND:", command)

    room = await Room.get(id=room_id)
    manager = build_manager(room.state)

    try:
        manager.send_command(command=command)
    except ExecuteCommandException as exp:
        print("ERROR IN EXECUTING:", exp)
        raise_command_exception(room_id, exp)
        return

    room.state = manager.game_state
    await room.save()
