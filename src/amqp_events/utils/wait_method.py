import asyncio
from typing import NewType, Callable
from amqp_events import AmqpEventListener


MessageFilter = NewType('MessageFilter', Callable[[dict], bool])


class ObserverWithFilter:
    _filter: MessageFilter
    _future: asyncio.Future

    def __init__(self, message_filter: MessageFilter):
        self._filter = message_filter
        self._future = asyncio.Future()

    async def __call__(self, message: dict):
        if self._filter(message):
            self._future.set_result(message)

    async def wait_for_message(self) -> dict:
        return await self._future


async def wait_for_publish(message_filter: MessageFilter, listener: AmqpEventListener):
    """
    Дожидается, когда произойдет событие, удовлетворяющее фильтру

    :param message_filter: фильтр сообщений
    :param listener: прослушиватель событий, к которому идет привязка
    """

    observer = ObserverWithFilter(message_filter)
    listener.attach(observer)
    result = await observer.wait_for_message()
    listener.detach(observer)
    return result
