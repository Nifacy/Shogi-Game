from enum import Enum


class RoomEvents(Enum):
    PLAYER_CONNECTED: str = "PLAYER_CONNECTED"
    GAME_STARTED: str = "GAME_STARTED"
    STATE_CHANGED: str = "STATE_CHANGED"


class CommandExecuteException(Enum):
    UNKNOWN_COMMAND: str = "UNKNOWN_COMMAND"
    EXECUTE_ERROR: str = "EXECUTE_ERROR"
