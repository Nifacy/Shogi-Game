from amqp_events import AmqpEventPublisher
from services.searcher_service.domain.events import searcher_events, OnFindOpponentMessage


amqp_publisher = AmqpEventPublisher(event_name='searcher_service.events')


async def on_find_opponent_publisher(message: OnFindOpponentMessage):
    print(f'[Event] Found opponent for {message.caller.name!r}!')

    await amqp_publisher.notify({
        'event_type': 'FOUND_OPPONENT',
        'caller': message.caller.name,
        'session_id': message.created_session.id
    })


searcher_events.on_find_opponent += on_find_opponent_publisher
