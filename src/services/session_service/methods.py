from contracts import session_service
from game_model.game.manager.exceptions import ExecuteCommandException
from services.session_service.command_parser import parse_command
from services.session_service.domain import adapters, models
from services.session_service.domain.usecases import *


class Implementation(session_service.Contract):
    def __init__(self, database: adapters.SessionStorage):
        self._database = database

    async def create_session(self, first_player: str, second_player: str) -> session_service.Session:
        created_session = await CreateSession(storage=self._database)(
            first_player_name=first_player,
            second_player_name=second_player)

        players = created_session.get_players()

        response = session_service.Session(
            session_id=created_session.id,
            first_player=players[0].name,
            second_player=players[1].name
        )
        return response

    async def connect_to_session(self, session_id: int, player_name: str):
        try:
            await ConnectToSession(storage=self._database)(session_id=session_id, player_name=player_name)

        except models.PlayerNotInSession:
            raise session_service.AccessDenied(session_id=session_id, player_name=player_name)

        except adapters.NotExists:
            raise session_service.NotExists(session_id=session_id)

    async def disconnect_from_session(self, session_id: int, player_name: str):
        try:
            await DisconnectFromSession(storage=self._database)(
                session_id=session_id,
                player_name=player_name)

        except models.PlayerNotInSession:
            raise session_service.AccessDenied(session_id=session_id, player_name=player_name)

        except adapters.NotExists:
            raise session_service.NotExists(session_id=session_id)

    async def execute_command(self, session_id: int, player_name: str, command: dict):
        try:
            player = await GetPlayer(self._database)(player_name, session_id)
            parsed_command = parse_command(player, command)
            await ExecuteCommand(self._database)(session_id, parsed_command)

        except ExecuteCommandException as e:
            raise session_service.ExecuteCommandError(description=str(e))

        except models.PlayerNotInSession:
            raise session_service.AccessDenied(session_id=session_id, player_name=player_name)

        except adapters.NotExists:
            raise session_service.NotExists(session_id=session_id)

    async def get_session_game_state(self, session_id: int) -> session_service.GameStateResponse:
        try:
            session = await GetSession(self._database)(session_id=session_id)

        except adapters.NotExists:
            raise session_service.NotExists(session_id=session_id)

        return session_service.GameStateResponse(state=session.state)
