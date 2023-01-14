from . import adapters, models, events


class CreatePrivateRoom:
    """Создает приватную комнату"""

    _storage: adapters.PrivateRoomStorage
    _builder: adapters.PrivateRoomBuilder

    def __init__(self, storage: adapters.PrivateRoomStorage, builder: adapters.PrivateRoomBuilder):
        self._storage = storage
        self._builder = builder

    async def __call__(self) -> models.PrivateRoom:
        room = await self._builder.generate_room()
        await self._storage.create_room(room.connection_key)
        await self._storage.update_room(room)
        return room


class DisconnectFromPrivateRoom:
    """
    Отключает игрока от приватной комнаты. Если все игроки отключились от приватной
    комнаты, она удаляется из хранилища
    """

    _storage: adapters.PrivateRoomStorage

    def __init__(self, storage: adapters.PrivateRoomStorage):
        self._storage = storage

    async def __call__(self, connection_key: models.ConnectionKey, player: models.Player):
        room = await self._storage.get_room(connection_key)
        room.remove_player(player=player)
        await self._storage.update_room(room)

        if room.is_empty():
            await self._storage.remove_room(room.connection_key)


class ConnectToPrivateRoom:
    """
    Подключает игрока к приватной комнате.
    В случае, если комната заполнилась, посылается запрос сервису сессий на
    создание игровой сессии и поднимается событие 'on_private_room_full'
    """

    _storage: adapters.PrivateRoomStorage
    _adapter: adapters.SessionServiceAdapter

    def __init__(self, storage: adapters.PrivateRoomStorage, adapter: adapters.SessionServiceAdapter):
        self._storage = storage
        self._adapter = adapter

    async def __call__(self, connection_key: models.ConnectionKey, player: models.Player):
        room = await self._storage.get_room(connection_key)
        room.add_player(player)
        await self._storage.update_room(room)

        if room.is_full():
            session = await self._adapter.create_session(room.players)
            message = events.OnPrivateRoomFullMessage(room=room, created_session=session)
            await events.private_room_events.on_private_room_full(message)
