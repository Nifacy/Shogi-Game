import asyncio
from dataclasses import dataclass
from starlette.websockets import WebSocket, WebSocketDisconnect
from contracts import session_service


@dataclass(frozen=True)
class ConnectionContext:
    websocket: WebSocket
    player_name: str
    session_id: int


class WebSocketCommandReceiver:
    _client: session_service.Contract
    _context: ConnectionContext

    def __init__(self, context: ConnectionContext, client: session_service.Contract):
        self._client = client
        self._context = context
        self._disconnect_future = asyncio.Future()

    async def _send_command(self, command: dict):
        try:
            await self._client.execute_command(
                session_id=self._context.session_id,
                player_name=self._context.player_name,
                command=command)
        except session_service.ExecuteCommandError as e:
            await self._context.websocket.send_text(str(e))

    async def start_listen(self):
        while True:
            try:
                command = await self._context.websocket.receive_json()
                await self._send_command(command)
            except WebSocketDisconnect:
                break


class WebSocketSessionEventObserver:
    _context: ConnectionContext

    def __init__(self, context: ConnectionContext):
        self._context = context

    def _validate_message(self, message: dict) -> bool:
        return message.get('session_id') == self._context.session_id

    async def __call__(self, message: dict):
        print(f'Got message: {message}')
        if self._validate_message(message):
            await self._context.websocket.send_json(message)
