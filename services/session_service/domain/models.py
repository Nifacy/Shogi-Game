from dataclasses import dataclass
from enum import Enum
from typing import Dict, Tuple

from game_model.game.manager.command import Command
from game_model.game.model import GameState, Player
from services.session_service.domain.factories import manager_factory


# Exceptions


class PlayerNotInSession(Exception):
    _tmp = "Player '{player_name}' not in session '{session_id}'"

    def __init__(self, session_id: int, player_name: str):
        super().__init__(self._tmp.format(session_id=session_id, player_name=player_name))
        self.session_id = session_id
        self.player_name = player_name


class PlayerConnectionState(Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"


# Models


@dataclass
class PlayerModel(Player):
    _name: str

    def __post_init__(self):
        super().__init__()
        print(f"Created player Player({self._name}, {self._id})")

    @property
    def name(self) -> str:
        return self._name

    def __repr__(self):
        return f"Player({self._name!r})"


@dataclass
class SessionModel:
    _session_id: int
    _players: Tuple[PlayerModel, PlayerModel]
    _player_connections: Dict[str, PlayerConnectionState]
    _state: GameState

    @property
    def id(self):
        return self._session_id

    @property
    def state(self) -> GameState:
        return self._state

    def get_player(self, player_name: str) -> PlayerModel:
        for player in self._players:
            if player.name == player_name:
                return player

        raise PlayerNotInSession(session_id=self.id, player_name=player_name)

    def get_players(self) -> Tuple[PlayerModel, PlayerModel]:
        return self._players

    def execute_command(self, command: Command):
        manager = manager_factory(self._state)
        manager.send_command(command)
        self._state = manager.game_state

    def connect(self, player_name: str):
        player = self.get_player(player_name)
        self._player_connections[player.name] = PlayerConnectionState.CONNECTED

    def disconnect(self, player_name: str):
        player = self.get_player(player_name)
        self._player_connections[player.name] = PlayerConnectionState.DISCONNECTED
