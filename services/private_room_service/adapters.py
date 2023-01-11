from pydantic import BaseModel

from rpc_service.client import BaseRpcClient


# Exceptions


class SessionNotExists(Exception):
    __tmp = "Session with {session_id} not exists"
    session_id: int

    def __init__(self, session_id: int):
        super().__init__(self.__tmp.format(session_id=session_id))
        self.session_id = session_id


class AccessDenied(Exception):
    __tmp = "Player '{player_name}' not in session {session_id}"
    player_name: str
    session_id: int

    def __init__(self, session_id: int, player_name: str):
        super().__init__(self.__tmp.format(player_name=player_name, session_id=session_id))
        self.player_name = player_name
        self.session_id = session_id


class ExecuteError(Exception):
    pass


# Schema


class Session(BaseModel):
    session_id: int
    first_player: str
    second_player: str


# Adapter


class SessionServiceAdapter(BaseRpcClient):
    def __init__(self):
        super().__init__(service_name="session_service", credentials="amqp://guest:guest@localhost")

    async def create_session(self, first_player: str, second_player: str) -> Session:
        result = await self._call("create", {"first_player": first_player, "second_player": second_player})
        return Session(**result)

    async def connect_to_session(self, session_id: int, player_name: str):
        result = await self._call("connect", {"session_id": session_id, "player_name": player_name})

        if result.get("message_type") == "success":
            return

        if result.get("error_type") == "not_exists":
            raise SessionNotExists(session_id)

        if result.get("error_type") == "access_denied":
            raise AccessDenied(session_id, player_name)

    async def disconnect_from_session(self, session_id: int, player_name: str):
        result = await self._call("disconnect", {"session_id": session_id, "player_name": player_name})

        if result.get("message_type") == "success":
            return

        if result.get("error_type") == "not_exists":
            raise SessionNotExists(session_id)

        if result.get("error_type") == "access_denied":
            raise AccessDenied(session_id, player_name)

    async def execute_command(self, session_id: int, player_name: str, command: dict):
        result = await self._call("disconnect", {"session_id": session_id, "player_name": player_name, "command": command})

        if result.get("message_type") == "success":
            return

        if result.get("error_type") == "not_exists":
            raise SessionNotExists(session_id)

        if result.get("error_type") == "access_denied":
            raise AccessDenied(session_id, player_name)

        if result.get("error_type", "").startswith("error.execute"):
            raise ExecuteError(result["detail"])
