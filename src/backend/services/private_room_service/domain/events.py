from dataclasses import dataclass
from aievents import Events
from . import models, adapters


@dataclass(frozen=True)
class OnPrivateRoomFullMessage:
    """
    Сообщение, посылаемое всем подписчикам на событие 'on_private_room_full'

    Arguments:
        room - комната, которая заполнилась
        created_session - созданная игровая сессия для игроков
    """

    room: models.PrivateRoom
    created_session: adapters.Session


class PrivateRoomEvents(Events):
    """
    События, происходящие во время выполнения в бизнес части

    Events:
        on_private_room_full - приватная комната заполнилась
    """

    __events__ = ('on_private_room_full', )


private_room_events = PrivateRoomEvents()
print('Initialized events')
