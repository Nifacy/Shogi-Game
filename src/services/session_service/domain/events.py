import pydantic
from aievents import Events

from game_model.game.model import GameState
from services.session_service.domain.models import PlayerModel


class OnPlayerConnectedMessage(pydantic.BaseModel):
    session_id: int
    player_name: str


class OnPlayerDisconnectedMessage(pydantic.BaseModel):
    session_id: int
    player_name: str


class OnStateChangedMessage(pydantic.BaseModel):
    session_id: int
    state: GameState


class OnGameEndedMessage(pydantic.BaseModel):
    session_id: int
    winner: PlayerModel


class SessionEvents(Events):
    __events__ = (
        'on_player_connected',
        'on_player_disconnected',
        'on_state_changed',
        'on_game_ended'
    )


session_events = SessionEvents()

