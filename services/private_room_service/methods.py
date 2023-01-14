from contracts import private_room_service
from services.private_room_service import domain
from services.private_room_service.domain import adapters, models


class Implementation(private_room_service.Contract):
    def __init__(self,
                 database: adapters.PrivateRoomStorage,
                 client: adapters.SessionServiceAdapter,
                 builder: adapters.PrivateRoomBuilder
    ):
        self._database = database
        self._client = client
        self._builder = builder

    async def create(self, player_name: str) -> private_room_service.PrivateRoomInfo:
        room = await domain.CreatePrivateRoom(self._database, self._builder)()
        await domain.ConnectToPrivateRoom(self._database, self._client)(room.connection_key, models.Player(player_name))
        return private_room_service.PrivateRoomInfo(connection_key=room.connection_key)

    async def connect_room(self, player_name: str, connection_key: str):
        try:
            await domain.ConnectToPrivateRoom(self._database, self._client)(connection_key, models.Player(player_name))

        except adapters.NotExists:
            raise private_room_service.RoomNotFound(connection_key=connection_key)

    async def disconnect_room(self, player_name: str, connection_key: str):
        try:
            await domain.DisconnectFromPrivateRoom(self._database)(
                connection_key=connection_key,
                player=models.Player(player_name))

        except adapters.NotExists:
            raise private_room_service.RoomNotFound(connection_key=connection_key)

        except models.NotConnected:
            raise private_room_service.PlayerNotConnected(connection_key=connection_key, player_name=player_name)
