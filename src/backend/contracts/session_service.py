from dataclasses import dataclass
import pydantic

from game_model.game.model import GameState
from rpc_service import ErrorResponse, RpcMessageGroup, ResponseMessage, RpcContract, endpoint
from state_encoder import StateEncoder


messages = RpcMessageGroup()


@messages.add_message_type
@dataclass
class AccessDenied(ErrorResponse):
    session_id: int
    player_name: str
    _message: str = 'Player {player_name!r} not connected to session {session_id!r}'


@messages.add_message_type
@dataclass
class NotExists(ErrorResponse):
    session_id: int
    _message: str = 'Session with id {session_id} not exists'


@messages.add_message_type
@dataclass
class ExecuteCommandError(ErrorResponse):
    description: str
    _message: str = 'Enable to execute command. Reason: {description}'


@messages.add_message_type
class Session(ResponseMessage):
    session_id: int
    first_player: str
    second_player: str


@messages.add_message_type
class GameStateResponse(ResponseMessage):
    state: GameState

    @pydantic.validator('state', pre=True)
    def _deserialize_state(cls, serialized):
        if isinstance(serialized, dict):
            return StateEncoder.decode(serialized)
        return serialized

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            GameState: StateEncoder.encode
        }


class Contract(RpcContract):
    __service__ = 'session_service'
    __messages__ = messages

    @endpoint
    async def create_session(self, first_player: str, second_player: str) -> Session:
        raise NotImplementedError()

    @endpoint
    async def connect_to_session(self, session_id: int, player_name: str):
        raise NotImplementedError()

    @endpoint
    async def disconnect_from_session(self, session_id: int, player_name: str):
        raise NotImplementedError()

    @endpoint
    async def execute_command(self, session_id: int, player_name: str, command: dict):
        raise NotImplementedError()

    @endpoint
    async def get_session_game_state(self, session_id: int) -> GameStateResponse:
        raise NotImplementedError()

print(f'>>>>>> {id(ExecuteCommandError)}')
