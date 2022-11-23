from enum import Enum


class RoomEvents(Enum):
    PLAYER_CONNECTED = "PLAYER_CONNECTED"
    GAME_STARTED = "GAME_STARTED"
    STATE_CHANGED = "STATE_CHANGED"


class CommandExecuteException(Enum):
    UNKNOWN_COMMAND = "UNKNOWN_COMMAND"
    EXECUTE_ERROR = "EXECUTE_ERROR"
