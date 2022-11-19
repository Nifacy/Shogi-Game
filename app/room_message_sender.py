import asyncio
from asyncio import AbstractEventLoop, Task

from ddd_domain_events import DomainEvents, DomainEventCallable
from fastapi.websockets import WebSocket

from app.events import RoomEvents, CommandExecuteException
from app.models import User
from app.state_converter import StateConverter
from game_model.game.model import GameState


class RoomMessageSender:
    _listen_room_id: int
    _user_id: int
    _connection: WebSocket

    _messages: list[str]
    _watch_message_task: Task

    def __init__(self, user_id: int, room_id: int, connection: WebSocket, events_context: DomainEvents, loop: AbstractEventLoop):
        self._listen_room_id = room_id
        self._connection = connection
        self._user_id = user_id
        self._messages = []

        events_context.register_event(
            domain_event_callable=DomainEventCallable(
                event_type=RoomEvents.PLAYER_CONNECTED,
                callback=self.on_player_connected
            )
        )

        events_context.register_event(
            domain_event_callable=DomainEventCallable(
                event_type=RoomEvents.GAME_STARTED,
                callback=self.on_game_started
            )
        )

        events_context.register_event(
            domain_event_callable=DomainEventCallable(
                event_type=RoomEvents.STATE_CHANGED,
                callback=self.on_state_change
            )
        )

        events_context.register_event(
            domain_event_callable=DomainEventCallable(
                event_type=CommandExecuteException.EXECUTE_ERROR,
                callback=self.on_command_execute_exception
            )
        )

        self._watch_message_task = loop.create_task(self._handle_incoming_messages())

    async def _send_message(self, message: str):
        await self._connection.send_text(message)

    async def _handle_incoming_messages(self):
        while True:
            if self._messages:
                await self._send_message(self._messages.pop())
            await asyncio.sleep(0.1)

    def on_player_connected(self, room_id: int, player: User):
        if room_id != self._listen_room_id:
            return

        self._messages.append(f"Player '{player.username}' connected!")

    def on_game_started(self, room_id: int):
        if room_id != self._listen_room_id:
            return

        self._messages.append("Gamed started!")

    def on_state_change(self, room_id: int, state: GameState):
        if room_id != self._listen_room_id:
            return

        self._messages.append(f"State changed: {StateConverter.encode(state)}")

    def on_command_execute_exception(self, detail: str, room_id: int, player_id: int):
        if player_id != self._user_id or room_id != self._listen_room_id:
            return

        self._messages.append(f"Command exception: {detail}")

    def stop(self):
        self._watch_message_task.cancel()
