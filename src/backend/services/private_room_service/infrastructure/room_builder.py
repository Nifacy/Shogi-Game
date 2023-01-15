import random
from ..domain import adapters, models


def _generate_connection_key() -> models.ConnectionKey:
    alph = 'ABCDEFGHIJKLMNOPQRCT'
    parts = []

    for _ in range(3):
        parts.append(''.join([random.choice(alph) for _ in range(3)]))

    return '-'.join(parts)


class DefaultRoomBuilder(adapters.PrivateRoomBuilder):
    _storage: adapters.PrivateRoomStorage

    def __init__(self, storage: adapters.PrivateRoomStorage):
        self._storage = storage

    async def generate_room(self) -> models.PrivateRoom:
        connection_key = _generate_connection_key()

        while True:
            try:
                await self._storage.get_room(connection_key)
            except adapters.NotExists:
                break

            connection_key = _generate_connection_key()

        return models.PrivateRoom(_players=[], _connection_key=connection_key)
