from amqp_events import AmqpEventPublisher
from services.session_service.domain.events import *
from state_encoder import StateEncoder

amqp_publisher = AmqpEventPublisher(event_name='session_service.sessions.events')


async def on_state_changed(message: OnStateChangedMessage):
    message = {
        "event_type": 'STATE_CHANGED',
        "session_id": message.session_id,
        "changed_state": StateEncoder.encode(message.state)
    }

    await amqp_publisher.notify(message)


async def on_player_connected(message: OnPlayerConnectedMessage):
    message = {
        "event_type": 'PLAYER_CONNECTED',
        "session_id": message.session_id,
        "player_name": message.player_name
    }

    await amqp_publisher.notify(message)


async def on_player_disconnected(message: OnPlayerDisconnectedMessage):
    message = {
        "event_type": 'PLAYER_DISCONNECTED',
        "session_id": message.session_id,
        "player_name": message.player_name
    }

    await amqp_publisher.notify(message)


async def on_game_ended(message: OnGameEndedMessage):
    message = {
        "event_type": SessionEvents.GAME_ENDED.value,
        "session_id": message.session_id,
        "winner": message.winner.name
    }

    await amqp_publisher.notify(message)


session_events.on_state_changed += on_state_changed
session_events.on_player_connected += on_player_connected
session_events.on_player_disconnected += on_player_disconnected
session_events.on_game_ended += on_game_ended
