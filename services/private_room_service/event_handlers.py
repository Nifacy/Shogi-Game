from amqp_events import AmqpEventPublisher
from .domain.events import private_room_events, OnPrivateRoomFullMessage


amqp_publisher = AmqpEventPublisher(event_name='private_room_service.events')


async def private_room_full_publisher(message: OnPrivateRoomFullMessage):
    print(f'[Event] Private room {message.room.connection_key!r} full!')

    await amqp_publisher.notify({
        'event_type': 'OPPONENT_CONNECTED',
        'connection_key': message.room.connection_key,
        'session_id': message.created_session.id
    })


def bind_handlers():
    private_room_events.on_private_room_full += private_room_full_publisher
